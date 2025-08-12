from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only for type checking
    from pyspark.sql import DataFrame, SparkSession


class ExternalSourceIngestion(ABC):
    """Abstract base for external source ingestion.

    Subclasses should implement `ingest` to fetch data from an
    external system into a local destination directory.

    Typical usage:
        ingestor = SomeIngestion(dest_dir="data/raw/external")
        files = ingestor.ingest()
    """

    def __init__(self, dest_dir: Path | str, spark: SparkSession | None = None) -> None:
        self.dest_dir = Path(dest_dir)
        self._spark = spark

    def _ensure_dest_dir(self) -> None:
        self.dest_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def source_name(self) -> str:
        """Short identifier for the external source (e.g., "kaggle")."""

    @abstractmethod
    def ingest(self) -> list[Path]:
        """Ingest data into `dest_dir` and return written file paths."""
        raise NotImplementedError

    @abstractmethod
    def to_spark(self, files: Sequence[Path]) -> DataFrame:
        """Load the ingested files into a Spark DataFrame."""
        raise NotImplementedError

    @property
    def spark(self) -> SparkSession:
        """SparkSession with Delta support.

        Subclasses can pass a SparkSession in the constructor; otherwise a
        default session is created lazily.
        """
        if self._spark is None:
            # Lazy import to avoid hard dependency at import time
            from mlops_e2e.spark import get_spark

            self._spark = get_spark()
        return self._spark

    def _normalize_identifier(self, name: str) -> str:
        """Normalize a string to a valid SQL identifier: lowercase, [a-z0-9_]."""
        # Replace non-word characters with underscore, then collapse repeats
        normalized = re.sub(r"\W+", "_", name.strip().lower())
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        if not normalized:
            raise ValueError("Empty identifier after normalization")
        return normalized

    def table_fqn(self, dataset: str) -> str:
        """Build a 3-part table name: external.<source>.<dataset>."""
        src = self._normalize_identifier(self.source_name())
        ds = self._normalize_identifier(dataset)
        return f"external.{src}.{ds}"

    def ensure_schema(self, source: str) -> None:
        """Ensure the `<catalog>.<schema>` exists for writes.

        Attempts to create `external.<source>` schema if it doesn't exist. If
        the environment doesn't support catalogs, this may no-op.
        """
        # Try creating external catalog schema if supported (Unity Catalog)
        schema_3p = f"external.{self._normalize_identifier(source)}"
        try:
            self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_3p}")
        except Exception:
            # Fall back quietly; schema may be managed externally or 2-part only
            pass

    def write_delta_table(
        self, df: DataFrame, dataset: str, mode: str = "overwrite"
    ) -> str:
        """Write DataFrame as a Delta table and return the table name.

        - Table name: `external.<source>.<dataset>`
        - Creates the schema if supported; ignores errors otherwise.
        - Uses `saveAsTable` to register in the metastore.
        """
        table = self.table_fqn(dataset)
        self.ensure_schema(self.source_name())
        df.write.format("delta").mode(mode).option("mergeSchema", "true").saveAsTable(
            table
        )
        return table

    def ingest_to_delta(self, dataset: str, mode: str = "overwrite") -> str:
        """End-to-end: ingest files, load to Spark, and write Delta table.

        Returns the fully-qualified table name written.
        """
        self._ensure_dest_dir()
        files = self.ingest()
        df = self.to_spark(files)
        return self.write_delta_table(df, dataset=dataset, mode=mode)
