from __future__ import annotations

from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

from ..base import ExternalSourceIngestion


class KaggleDatasetIngestion(ExternalSourceIngestion):
    """Ingests a Kaggle dataset into a local directory.

    Parameters
    - dataset: Kaggle dataset slug in the form "owner/dataset".
    - dest_dir: Local directory to download files into.
    - unzip: Whether to unzip the dataset archive. Default True.
    - quiet: Reduce Kaggle API output. Default True.

    Notes
    - Requires Kaggle credentials (~/.kaggle/kaggle.json) or env vars
      KAGGLE_USERNAME and KAGGLE_KEY.
    - Returns a list of Paths for downloaded files. If `unzip=False`,
      the returned list will contain the single archive file path.
    """

    def __init__(
        self,
        dataset: str,
        dest_dir: Path | str,
        *,
        unzip: bool = True,
        quiet: bool = True,
        force: bool = False,
    ) -> None:
        super().__init__(dest_dir)
        if "/" not in dataset:
            raise ValueError(
                "dataset must be in the form 'owner/dataset', e.g., 'zynicide/wine-reviews'"
            )
        self.dataset = dataset
        self.unzip = unzip
        self.quiet = quiet
        self.force = force

    def ingest(self) -> list[Path]:
        self._ensure_dest_dir()

        api = KaggleApi()
        api.authenticate()

        # Kaggle API writes directly to the provided path. If unzip is False,
        # it writes a single .zip file and returns nothing; we compute paths below.
        api.dataset_download_files(
            self.dataset,
            path=str(self.dest_dir),
            unzip=self.unzip,
            quiet=self.quiet,
            force=self.force,
        )

        if self.unzip:
            return _list_files_recursive(self.dest_dir)
        else:
            slug = self.dataset.split("/")[1]
            archive = self.dest_dir / f"{slug}.zip"
            return [archive]


def _list_files_recursive(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file():
            files.append(p)
    return files
