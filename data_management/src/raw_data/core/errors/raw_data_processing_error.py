"""
This module defines custom exception classes for better error management and logging
in the TableToDBService class. It includes exceptions for invalid file names and 
processing errors.
"""

class InvalidFileNameError(Exception):
    """
    Raised when an invalid file name is encountered in the processing pipeline.

    """

class ProcessingError(Exception):
    
  """  
  Raised when an error occurs during the processing of raw data files.
  """


class DataInsertionError(Exception):
    """
    Raised when an error occurs during the Data insertion.
    """
