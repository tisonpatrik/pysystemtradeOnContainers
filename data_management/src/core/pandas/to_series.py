import pandas as pd
from src.core.errors.conversion_errors import DataFrameConversionError
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_frame_to_series(
    data_frame: pd.DataFrame, index_column: str, price_column: str
) -> pd.Series:
    """
    Converts a specified column of a Pandas DataFrame to a Pandas Series with another column as its index.
    """
    try:
        # Set the specified column as the index
        indexed_df = data_frame.set_index(index_column)

        # Extract the Series
        series = indexed_df[price_column]

        # Resample if the index is datetime, comment out if not needed
        if pd.api.types.is_datetime64_any_dtype(indexed_df.index):
            series = series.resample("1B").last()

        return series
    except Exception as e:
        logger.error("Error during conversion to Pandas Series: %s", e)
        raise DataFrameConversionError(f"An error occurred during conversion: {e}")
