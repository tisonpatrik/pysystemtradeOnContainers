"""
Module for defining custom exceptions related to date and time operations in data aggregation.
"""


class InvalidDatetimeColumnError(Exception):
    """Raised when the specified column cannot be converted to datetime."""


class DateTimeConversionError(Exception):
    """Raised when there's an error in converting date/time."""


class DataPreparationError(Exception):
    """Exception raised for errors in the data preparation process."""
