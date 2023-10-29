# dataframe_to_series_errors.py


class DataFrameToSeriesError(Exception):
    """Base class for all DataFrame to Series conversion errors."""

    pass


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

    pass


class DataFrameConversionError(DataFrameToDictOfSeriesError):
    """Raised when an error occurs during DataFrame to Series conversion."""

    def __init__(self, error: Exception):
        self.original_error = error
        super().__init__(
            f"An error occurred while converting DataFrame to Series: {error}"
        )
