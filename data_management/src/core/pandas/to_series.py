import pandas as pd
import polars as pl
from src.core.errors.conversion_errors import DataFrameConversionError
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_polars_to_series(
    data_frame: pl.DataFrame, index_column: str, price_column: str
) -> pd.Series:
    """
    Converts a specified column of a Polars DataFrame to a Pandas Series with another column as its index.
    """
    try:
        # Convert the specified column to datetime format
        converted_df: pd.DataFrame = data_frame.to_pandas()
        indexed_df = converted_df.set_index(index_column)
        series = indexed_df[price_column]
        return series
    except Exception as e:
        # Raise a custom error for any exceptions that may occur
        raise DataFrameConversionError(f"An error occurred during conversion: {e}")
