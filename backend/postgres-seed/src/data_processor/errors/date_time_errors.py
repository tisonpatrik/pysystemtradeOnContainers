"""
bla
"""

class DataAggregationError(Exception):
    """Raised when there's an error in data aggregation."""

class InvalidDatetimeColumnError(Exception):
    """Raised when the specified column cannot be converted to datetime."""

class DateTimeConversionError(Exception):
    """Raised when there's an error in converting date/time."""