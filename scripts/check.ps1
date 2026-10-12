# Local quality gate. Run before every commit. No CI runs in the cloud.
$ErrorActionPreference = "Stop"

python scripts/generate_table.py --check
if ($LASTEXITCODE) { exit 1 }
ruff format --check .
if ($LASTEXITCODE) { exit 1 }
ruff check .
if ($LASTEXITCODE) { exit 1 }
mypy --strict src
if ($LASTEXITCODE) { exit 1 }
pytest
if ($LASTEXITCODE) { exit 1 }
