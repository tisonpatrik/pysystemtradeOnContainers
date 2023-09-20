"""
Module containing custom exceptions related to database interactions.

These exceptions provide more granular error handling for database operations,
such as syntax errors, connection issues, and missing entities.
"""

class EntityDoesNotExist(Exception):
    """Raised when an entity was not found in the database."""

class DatabaseConnectionError(Exception):
    """Raised when there's a connection error to the database."""

class DatabaseInteractionError(Exception):
    """Raised when there's an error interacting with the database."""

class SQLSyntaxError(DatabaseInteractionError):
    """Raised when there's a syntax error in the SQL command."""

class TableOrColumnNotFoundError(DatabaseInteractionError):
    """Raised when a specified table or column doesn't exist in the database."""

class ParameterMismatchError(DatabaseInteractionError):
    """Raised when there's a parameter mismatch in the SQL command."""
