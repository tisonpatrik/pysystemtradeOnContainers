"""Custom exceptions for handling errors during DataFrame to Series conversion."""


class DataFrameToSeriesError(Exception):
    """Base class for all DataFrame to Series conversion errors."""

    def __init__(self, message: str):
        super().__init__(message)


class ColumnNotFoundError(DataFrameToSeriesError):
    """Raised when a required column is not found in the DataFrame."""

    def __init__(self, column_name: str):
        self.column_name = column_name
        super().__init__(f"Failed to find column {column_name} in DataFrame")


class GroupByError(DataFrameToSeriesError):
    """Raised when there's an issue with the groupby operation."""

    def __init__(self, error: Exception):
        self.original_error = error
        super().__init__(f"An error occurred during the groupby operation: {error}")


class DataFrameToDictOfSeriesError(DataFrameToSeriesError):
    """Base class for errors during DataFrame to dictionary of Series conversion."""


class DataFrameConversionError(DataFrameToDictOfSeriesError):
    """Raised when an error occurs during DataFrame to Series conversion."""

    def __init__(self, error: Exception):
        self.original_error = error
        super().__init__(
            f"An error occurred while converting DataFrame to Series: {error}"
        )
