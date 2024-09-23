# common/src/dependencies/errors/dependencies_errors.py


class DatabaseError(Exception):
    """Base class for all database-related errors."""


class DatabaseInitializationError(DatabaseError):
    """Raised when the database connection pool fails to initialize."""

    def __init__(self, message: str = "Failed to initialize the database connection pool.", original_exception: Exception | None = None):
        super().__init__(message)
        self.original_exception = original_exception


class DatabaseConnectionError(DatabaseError):
    """Raised when there is an issue with the database connection."""

    def __init__(self, message: str = "Database connection error.", original_exception: Exception | None = None):
        super().__init__(message)
        self.original_exception = original_exception
