class DatabaseError(Exception):
    """Base exception for repository errors."""


class FetchError(DatabaseError):
    """Exception raised for errors during fetch operations."""


class InsertError(DatabaseError):
    """Exception raised for errors during insert operations."""
