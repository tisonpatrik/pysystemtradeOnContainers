class RepositoryError(Exception):
    """Base exception for repository errors."""


class FetchError(RepositoryError):
    """Exception raised for errors during fetch operations."""


class InsertError(RepositoryError):
    """Exception raised for errors during insert operations."""
