from .base import ExternalSourceIngestion

# Re-export Kaggle dataset ingestor for convenience
try:
    from .kaggle import KaggleDatasetIngestion  # noqa: F401
except Exception:  # pragma: no cover - optional at import time
    # Kaggle may not be installed in minimal environments.
    pass

__all__ = ["ExternalSourceIngestion"]
