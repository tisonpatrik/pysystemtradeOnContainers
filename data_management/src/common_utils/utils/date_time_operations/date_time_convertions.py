"""
Module for date-time related conversion utilities.
"""

import time
import pandas as pd
import polars as pl

from src.core.errors.date_time_errors import DateTimeConversionError,InvalidDatetimeColumnError

from src.utils.logging import AppLogger
logger = AppLogger.get_instance().get_logger()


def convert_string_column_to_datetime(data_frame: pl.DataFrame, date_time_column: str) -> pd.DataFrame:
    """
    Converts a specified column in the DataFrame to datetime format.
    """
    try:
        # Convert the specified column to datetime format
        converted_df = data_frame.with_columns(pl.col(date_time_column).str.strptime(pl.Datetime, None))
        return converted_df
    except Exception as exc:
        logger.error("Failed to convert column %s to datetime: %s", date_time_column, exc)
        raise InvalidDatetimeColumnError(f"Failed to convert {date_time_column} to datetime") from exc

def convert_datetime_to_unixtime(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Converts the date_column to UNIX time.
    """
    try:
        data_frame[date_time_column] = data_frame[date_time_column].apply(
            lambda x: int(time.mktime(x.timetuple()))
        )
        return data_frame
    except Exception as error:
        logger.error("Error during unix_date_time conversion: %s", error)
        raise DateTimeConversionError from error
