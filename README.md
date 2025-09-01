MLOps E2E

Quick Start
- Install `uv`: macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Create venv (Python 3.12.3): `uv venv --python 3.12.3`
- Install deps (enforce lockfile): `uv sync --frozen --extra dev`
- Install hooks: `uv run pre-commit install`

Common Commands
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run black .`
- Type check: `uv run mypy`

Requirements
- Python 3.12.3
- Databricks Connect 16.4.2 (provided via project dependencies)
- No local Java required for Connect-based development

Spark + Delta Notes
- This project uses Databricks Connect `16.4.2` for local development against a Databricks workspace.
- Create the Spark session via Connect and pass it when needed:
  ```python
  from databricks.connect import DatabricksSession
  from pyspark.dbutils import DBUtils

  spark = DatabricksSession.builder.getOrCreate()
  dbutils = DBUtils(spark)
  ```
- For true local Spark (no Connect), install the `local` extra: `uv sync --extra local`.

CI
- GitHub Actions runs pre-commit (lint/format/type) and pytest on pushes/PRs to `main`.
- Pre-commit environments are cached for faster runs.
 - Lockfile: `uv.lock` is committed. CI enforces it with `uv sync --frozen --extra dev`.
   - For local reproducible installs, you can also use `uv sync --frozen`.
   - When changing dependencies, use `uv add ...` (or `uv sync`) to update `uv.lock`.

External Ingestion → Delta
- Base class: `mlops_e2e.ingestion.external.ExternalSourceIngestion`.
- Subclasses implement:
  - `source_name() -> str` (e.g., `"kaggle"`).
  - `ingest() -> list[Path]` to download files into a local `dest_dir`.
  - `to_spark(files) -> pyspark.sql.DataFrame` to load files as a DataFrame.
- Writing: call `ingest_to_delta(dataset="<dataset_name>")` or use
  `write_delta_table(df, dataset)` directly.
- Table name: `external.<source>.<dataset>`; schema is created if supported.

Kaggle Example
- Ensure `kaggle` credentials are configured (env vars or `~/.kaggle/kaggle.json`).
- Ingest Chicago Taxi Trips (`datasets/chicago/chicago-taxi-trips-bq/`):
  - Python:
    ```python
    from pathlib import Path
    from mlops_e2e.ingestion.external import KaggleDatasetIngestion
    from databricks.connect import DatabricksSession

    spark = DatabricksSession.builder.getOrCreate()
    ingestor = KaggleDatasetIngestion(
        dataset="datasets/chicago/chicago-taxi-trips-bq/",
        dest_dir=Path("data/external/kaggle/chicago_taxi_trips_bq"),
        spark=spark,
    )
    table = ingestor.ingest_to_delta(dataset="chicago_taxi_trips_bq")
    # Writes Delta table: external.kaggle.chicago_taxi_trips_bq
    ```
