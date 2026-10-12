# Contributing

Thanks for taking the time. This project keeps a small, predictable shape.

## Setup

```
pip install -r requirements-dev.txt
```

## Before you open a pull request

- Keep public API in `src/mimeguess/__init__.py`; internals live in `_`-prefixed modules.
- Never edit `src/mimeguess/_data.json.gz` or `_meta.py` by hand. Change the
  snapshot (see `data/README.md`) or `scripts/_supplement.py`, then run
  `python scripts/generate_table.py`.
- Add a test for the behaviour you change. Unit tests need no network; the end to
  end test builds the real wheel and installs it into a throwaway virtual
  environment (pip may fetch the build backend if it is not installed).
- Run `scripts/check.ps1` (generated table check, format, lint, types, tests) and
  make sure it passes.
- One logical change per commit, imperative subject line.

Open an issue first if the change is large or shifts the public API.
