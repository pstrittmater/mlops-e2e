MLOps E2E

Quick Start
- Install `uv`: macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Create venv: `uv venv --python 3.12`
- Install deps: `uv sync --extra dev`
- Install hooks: `uv run pre-commit install`

Common Commands
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run black .`
- Type check: `uv run mypy`

Requirements
- Python 3.12
- Java 11 or 17 (for PySpark 3.5)
- Optional: set `JAVA_HOME` for consistent Spark behavior

Spark + Delta Notes
- This project depends on `pyspark>=3.5,<3.6` and `delta-spark==3.3.0`.
- The first Delta-enabled Spark session may download JARs from Maven.

CI
- GitHub Actions runs pre-commit (lint/format/type) and pytest on pushes/PRs to `main`.
- Pre-commit environments are cached for faster runs.
