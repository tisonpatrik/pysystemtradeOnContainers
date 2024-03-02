import pandas as pd

from common.logging.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def convert_series_to_frame(series: pd.Series) -> pd.DataFrame:
    """
    Converts a Pandas Series to a Pandas DataFrame.
    """
    try:
        # Convert the Series to a DataFrame first
        data_frame = series.reset_index()
        return data_frame

    except Exception as exc:
        error_message = f"An error occurred during conversion {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)


def convert_frame_to_series(
    data_frame: pd.DataFrame, index_column: str, price_column: str
) -> pd.Series:
    """
    Converts a specified column of a Polars DataFrame to a Pandas Series with another column as its index.
    """
    try:
        # Convert the specified column to datetime format
        indexed_df = data_frame.set_index(index_column)
        series = indexed_df.resample("1B").last()
        series = indexed_df[price_column]
        return series

    except Exception as exc:
        error_message = f"An error occurred during conversion {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)
