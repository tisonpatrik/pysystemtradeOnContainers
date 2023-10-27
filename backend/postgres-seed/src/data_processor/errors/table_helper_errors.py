"""
Module for defining custom exceptions related to DataFrame column manipulations and operations.
"""


class ColumnRenameError(Exception):
    """Raised when there's an error while renaming DataFrame columns."""


class MissingColumnsError(Exception):
    """Raised when there are missing columns in the DataFrame."""


class SymbolAdditionError(Exception):
    """Raised when there's an error in adding a 'symbol' column to the DataFrame."""


class ColumnRoundingError(Exception):
    """Exception raised for errors occurring during column rounding."""
