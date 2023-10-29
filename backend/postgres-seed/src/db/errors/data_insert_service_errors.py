"""
This module defines custom exceptions for the DataInsertService.
These exceptions provide more specific error handling for database insert operations.
"""


class DataInsertServiceError(Exception):
    """Base exception for DataInsertService."""


class DataFrameInsertError(DataInsertServiceError):
    """Raised when there is an issue inserting a DataFrame into the database."""


class TransactionCommitError(DataInsertServiceError):
    """Raised when there is an issue committing a transaction to the database."""
