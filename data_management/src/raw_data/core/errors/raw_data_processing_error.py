"""
This module defines custom exception classes for better error management and logging
in the TableToDBService class. It includes exceptions for invalid file names and 
processing errors.
"""

class ProcessingError(Exception):
    
  """  
  Raised when an error occurs during the processing of raw data files.
  """

class PricesFilesProcessingError(Exception):
    """Exception raised for errors during the processing of multiple CSV files in PricesService."""


