from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, cast

from ..base import ExternalSourceIngestion

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from pyspark.sql import DataFrame


class KaggleDatasetIngestion(ExternalSourceIngestion):
    """Ingest a Kaggle dataset and (optionally) write to a Delta table.

    Parameters
    - dataset: Kaggle dataset ref "owner/dataset" (optionally prefixed with
      "datasets/"; trailing slash allowed).
    - dest_dir: Local directory to download files into.
    - unzip: Whether to unzip the dataset archive. Default True.
    - quiet: Reduce Kaggle API output. Default True.
    - force: Force re-download in Kaggle API. Default False.
    - spark: Optional SparkSession; if not provided, created lazily when needed.

    Notes
    - Requires Kaggle credentials (~/.kaggle/kaggle.json) or env vars
      KAGGLE_USERNAME and KAGGLE_KEY.
    - `ingest()` returns a list of Paths for downloaded files. If `unzip=False`,
      the returned list will contain the single archive file path.
    - Use `ingest_to_delta(dataset=...)` from the base class to write to
      `external.kaggle.<dataset>`.
    """

    def __init__(
        self,
        dataset: str,
        dest_dir: Path | str,
        *,
        unzip: bool = True,
        quiet: bool = True,
        force: bool = False,
        spark=None,
    ) -> None:
        super().__init__(dest_dir, spark=spark)
        self.dataset = self._normalize_ref(dataset)
        self.unzip = unzip
        self.quiet = quiet
        self.force = force

    def source_name(self) -> str:
        return "kaggle"

    def _normalize_ref(self, ref: str) -> str:
        ref = ref.strip().rstrip("/")
        if ref.startswith("datasets/"):
            ref = ref[len("datasets/") :]
        if "/" not in ref or ref.count("/") != 1:
            raise ValueError(
                "dataset must be in the form 'owner/dataset', e.g., 'chicago/chicago-taxi-trips-bq'"
            )
        return ref

    def ingest(self) -> list[Path]:
        self._ensure_dest_dir()
        # Lazy import to avoid hard dependency at module import time
        from kaggle.api.kaggle_api_extended import KaggleApi

        # Kaggle API writes directly to the provided path. If unzip is False,
        # it writes a single .zip file and returns nothing; we compute paths below.
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(
            self.dataset,
            path=str(self.dest_dir),
            unzip=self.unzip,
            quiet=self.quiet,
            force=self.force,
        )

        if self.unzip:
            return self._list_files_recursive(self.dest_dir)
        else:
            slug = self.dataset.split("/")[1]
            archive = self.dest_dir / f"{slug}.zip"
            return [archive]

    def _list_files_recursive(self, root: Path) -> list[Path]:
        files: list[Path] = []
        for p in root.rglob("*"):
            if p.is_file():
                files.append(p)
        return files

    def _select_files(self, files: Sequence[Path], *suffixes: str) -> list[Path]:
        sfx = tuple(s.lower() for s in suffixes)
        return [p for p in files if p.suffix.lower() in sfx]

    def to_spark(self, files: Sequence[Path]) -> DataFrame:
        # Prefer Parquet if present, otherwise CSV
        pq_files = self._select_files(files, ".parquet")
        if pq_files:
            return self.spark.read.parquet(*[str(p) for p in pq_files])

        csv_files = self._select_files(files, ".csv")
        if csv_files:
            df: DataFrame | None = None
            for p in csv_files:
                part = (
                    self.spark.read.option("header", True)
                    .option("inferSchema", True)
                    .csv(str(p))
                )
                df = (
                    part
                    if df is None
                    else df.unionByName(part, allowMissingColumns=True)
                )
            return cast("DataFrame", df)

        raise ValueError(
            "Unsupported file types for Kaggle dataset; expected Parquet or CSV files."
        )
