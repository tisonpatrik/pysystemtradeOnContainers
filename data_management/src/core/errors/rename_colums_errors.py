"""
Module for defining custom exceptions related to DataFrame column manipulations and operations.
"""


class ColumnRenameError(Exception):
    """Raised when there's an error while renaming DataFrame columns."""
