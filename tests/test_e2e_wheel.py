"""Build the real wheel, install it into a throwaway venv and drive the real script."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import venv
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def installed(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    """Yield the path of the installed ``mimeguess`` console script."""
    work = tmp_path_factory.mktemp("e2e")
    wheels = work / "wheels"
    # Reuse a locally installed build backend when there is one, so the test also
    # works offline; otherwise pip fetches hatchling into an isolated environment.
    isolation = ["--no-build-isolation"] if importlib.util.find_spec("hatchling") else []
    command = [sys.executable, "-m", "pip", "wheel", "--no-deps", "-q", *isolation]
    subprocess.run([*command, "-w", str(wheels), str(ROOT)], check=True)
    (wheel,) = wheels.glob("mimeguess-*.whl")
    env_dir = work / "venv"
    venv.EnvBuilder(with_pip=True).create(env_dir)
    bin_dir = env_dir / ("Scripts" if os.name == "nt" else "bin")
    python = bin_dir / ("python.exe" if os.name == "nt" else "python")
    subprocess.run([str(python), "-m", "pip", "install", "-q", str(wheel)], check=True)
    yield bin_dir / ("mimeguess.exe" if os.name == "nt" else "mimeguess")


def cli(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(script), *args], capture_output=True, text=True, timeout=120, check=False
    )


def test_the_installed_script_reports_the_version(installed: Path) -> None:
    from mimeguess import __version__

    result = cli(installed, "--version")
    assert result.returncode == 0
    assert result.stdout.strip() == f"mimeguess {__version__}"


def test_the_installed_script_guesses_types(installed: Path) -> None:
    result = cli(installed, "type", "report.pdf", "site.tar.gz", "index.html")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines == [
        "report.pdf\tapplication/pdf",
        "site.tar.gz\tapplication/gzip",
        "index.html\ttext/html",
    ]
    result = cli(installed, "type", "--encoding", "site.tar.gz")
    assert result.stdout == "application/x-tar\tgzip\n"


def test_the_installed_script_lists_extensions(installed: Path) -> None:
    result = cli(installed, "ext", "image/jpeg")
    assert result.returncode == 0 and result.stdout == ".jpg .jpeg .jpe\n"


def test_the_installed_script_sniffs_a_real_file(installed: Path, tmp_path: Path) -> None:
    target = tmp_path / "blob.bin"
    target.write_bytes(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
    result = cli(installed, "sniff", str(target))
    assert result.returncode == 0 and result.stdout == "application/pdf\n"


def test_the_installed_script_reports_its_data_source(installed: Path) -> None:
    result = cli(installed, "source", "--json")
    data = json.loads(result.stdout)
    assert data["name"] == "mime-db" and data["type_count"] > 2500


def test_the_installed_script_fails_cleanly(installed: Path) -> None:
    result = cli(installed, "type", "no.such-extension")
    assert result.returncode == 1 and result.stdout == ""
    assert "no MIME type known" in result.stderr
    result = cli(installed, "frobnicate")
    assert result.returncode == 1 and "invalid choice" in result.stderr


def test_the_installed_wheel_carries_the_table_and_notices(installed: Path) -> None:
    python = installed.parent / installed.name.replace("mimeguess", "python")
    code = (
        "import importlib.metadata as m, mimeguess; "
        "files = [str(f) for f in m.files('mimeguess')]; "
        "print(mimeguess.guess_type('x.webp')); "
        "print(any(f.endswith('_data.json.gz') for f in files)); "
        "print(sum(f.endswith(('mime-db.txt', 'mime-types.txt')) for f in files))"
    )
    result = subprocess.run([str(python), "-c", code], capture_output=True, text=True, check=True)
    assert result.stdout.split() == ["image/webp", "True", "2"]
