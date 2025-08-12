from .base import ExternalSourceIngestion

# Re-export Kaggle dataset ingestor for convenience
try:  # pragma: no cover - import may fail if kaggle missing
    from .kaggle import KaggleDatasetIngestion  # noqa: F401

    __all__ = ["ExternalSourceIngestion", "KaggleDatasetIngestion"]
except Exception:  # pragma: no cover - optional at import time
    # Kaggle may not be installed in minimal environments.
    __all__ = ["ExternalSourceIngestion"]
