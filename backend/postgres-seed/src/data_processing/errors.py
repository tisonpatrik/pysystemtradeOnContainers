"""
This module defines custom exception classes for error handling within the data processing workflow.
Each exception type corresponds to a specific kind of error that can occur during data loading, 
manipulation, or conversion.
"""

class CSVFileNotFoundError(Exception):
    """Raised when a CSV file is not found."""
class CSVFileLoadingError(Exception):
    """Raised when there's an error in loading the CSV file.""" 
class ColumnRenamingError(Exception):
    """Raised when there's an error in renaming columns.""" 
class DataAggregationError(Exception):
    """Raised when there's an error in data aggregation."""
class DateTimeConversionError(Exception):
    """Raised when there's an error in converting date/time."""
class EmptyDataFrameError(Exception):
    """Raised when a DataFrame is empty or contains only null values."""
class EmptyValueFillError(Exception):
    """Raised when there's an error in filling empty DataFrame values."""
class SymbolAdditionError(Exception):
    """Raised when there's an error in adding a 'symbol' column to the DataFrame."""
class ColumnRenameError(Exception):
    """Raised when there's an error while renaming DataFrame columns."""
