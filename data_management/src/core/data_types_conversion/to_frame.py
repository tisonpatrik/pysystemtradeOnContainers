import pandas as pd
import polars as pl
from src.core.errors.conversion_errors import DataFrameConversionError
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_series_to_frame(series: pd.Series) -> pl.DataFrame:
    """
    Converts a Pandas Series to a Polars DataFrame.
    """
    try:
        # Convert the Series to a DataFrame first
        pandas_df = series.reset_index()
        # Convert the Pandas DataFrame to a Polars DataFrame
        polars = pl.DataFrame(pandas_df)
        return polars

    except Exception as e:
        # Raise a custom error for any exceptions that may occur
        raise DataFrameConversionError(f"An error occurred during conversion: {e}")
