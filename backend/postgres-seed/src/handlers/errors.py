"""
Module to handle custom exceptions for the application.
"""

class ProcessingError(Exception):
    """An error occurred while processing the data."""

class DatabaseError(Exception):
    """Failed to reset the database."""