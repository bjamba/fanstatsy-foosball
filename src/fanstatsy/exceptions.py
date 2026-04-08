"""Custom exception classes for Fanstatsy Foosball."""


class FanstatsyError(Exception):
    """Base exception for all Fanstatsy errors."""


class DataQualityError(FanstatsyError):
    """Raised when data fails validation checks."""


class IngestionError(FanstatsyError):
    """Raised when a data source fails to respond or returns unexpected data."""


class ModelError(FanstatsyError):
    """Raised when model training or inference fails."""
