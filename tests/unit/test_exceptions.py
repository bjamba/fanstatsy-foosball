"""Tests for custom exception classes."""

import pytest

from fanstatsy.exceptions import (
    DataQualityError,
    FanstatsyError,
    IngestionError,
    ModelError,
)


def test_fanstatsy_error_is_exception() -> None:
    """FanstatsyError should be a subclass of Exception."""
    with pytest.raises(FanstatsyError):
        raise FanstatsyError("test error")


def test_data_quality_error_inherits_from_base() -> None:
    """DataQualityError should be catchable as FanstatsyError."""
    with pytest.raises(FanstatsyError):
        raise DataQualityError("bad data")


def test_ingestion_error_inherits_from_base() -> None:
    """IngestionError should be catchable as FanstatsyError."""
    with pytest.raises(FanstatsyError):
        raise IngestionError("source down")


def test_model_error_inherits_from_base() -> None:
    """ModelError should be catchable as FanstatsyError."""
    with pytest.raises(FanstatsyError):
        raise ModelError("training failed")


def test_exceptions_carry_message() -> None:
    """All custom exceptions should carry their message."""
    error = DataQualityError("missing columns: player_id")
    assert str(error) == "missing columns: player_id"
