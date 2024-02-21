import pandas as pd
import polars as pl
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_frame_to_series(
    data_frame: pl.DataFrame, index_column: str, price_column: str
) -> pd.Series:
    """
    Converts a specified column of a Polars DataFrame to a Pandas Series with another column as its index.
    """
    try:
        # Convert the specified column to datetime format
        converted_df = data_frame.to_pandas()
        indexed_df = converted_df.set_index(index_column)
        series = indexed_df.resample("1B").last()
        series = indexed_df[price_column]
        return series

    except Exception as exc:
        error_message = f"An error occurred during conversion {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)
