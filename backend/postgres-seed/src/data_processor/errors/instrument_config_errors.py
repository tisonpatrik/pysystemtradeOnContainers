"""
Module to define custom exceptions used across the application for better error handling and logging.
"""

class InvalidFileNameError(Exception):
    """
    Raised when the provided file name or path is invalid or does not exist.
    """

class ProcessingError(Exception):
    """
    Raised when an error occurs during the processing of data.
    """