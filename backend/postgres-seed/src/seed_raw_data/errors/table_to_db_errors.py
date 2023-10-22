"""
This module defines custom exception classes for better error management and logging
in the TableToDBService class. It includes exceptions for invalid file names and 
processing errors.
"""

class InvalidFileNameError(Exception):
    """
    Raised when an invalid file name is encountered in the processing pipeline.
    
    Attributes:
        message -- explanation of the error
    """

class ProcessingError(Exception):
    """
    Raised when an error occurs during the processing of raw data files.
    
    Attributes:
        message -- explanation of the error
    """
