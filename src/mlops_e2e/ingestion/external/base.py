from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ExternalSourceIngestion(ABC):
    """Abstract base for external source ingestion.

    Subclasses should implement `ingest` to fetch data from an
    external system into a local destination directory.

    Typical usage:
        ingestor = SomeIngestion(dest_dir="data/raw/external")
        files = ingestor.ingest()
    """

    def __init__(self, dest_dir: Path | str) -> None:
        self.dest_dir = Path(dest_dir)

    def _ensure_dest_dir(self) -> None:
        self.dest_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def ingest(self) -> list[Path]:
        """Ingest data into `dest_dir` and return written file paths."""
        raise NotImplementedError
