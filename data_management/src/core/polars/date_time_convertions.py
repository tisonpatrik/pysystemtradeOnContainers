"""
Module for date-time related conversion utilities.
"""
import time

import pandas as pd
from src.core.utils.logging import AppLogger
from src.raw_data.errors.date_time_errors import (
    DateTimeConversionError,
    InvalidDatetimeColumnError,
)

logger = AppLogger.get_instance().get_logger()


def convert_string_column_to_datetime(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Converts a specified column in the Pandas DataFrame to datetime format.
    """
    try:
        data_frame[date_time_column] = pd.to_datetime(data_frame[date_time_column])
        return data_frame
    except Exception as exc:
        logger.error(
            "Failed to convert column %s to datetime: %s", date_time_column, exc
        )
        raise InvalidDatetimeColumnError(
            f"Failed to convert {date_time_column} to datetime"
        ) from exc


def convert_datetime_to_unixtime(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Converts the datetime column to UNIX time in the Pandas DataFrame.
    """
    try:
        # Convert the specified column to datetime format if it's not already
        if not pd.api.types.is_datetime64_any_dtype(data_frame[date_time_column]):
            data_frame[date_time_column] = pd.to_datetime(data_frame[date_time_column])

        # Convert datetime to UNIX time using time module
        data_frame[date_time_column] = data_frame[date_time_column].apply(
            lambda x: int(time.mktime(x.timetuple()))
        )
        return data_frame

    except Exception as error:
        logger.error("Error during unix_date_time conversion: %s", error)
        raise DateTimeConversionError from error


def convert_and_sort_by_time(data_frame: pd.DataFrame, date_time_column: str):
    try:
        data_frame[date_time_column] = pd.to_datetime(data_frame[date_time_column])
        data_frame = data_frame.sort_values(by=date_time_column)
        return data_frame
    except Exception as error:
        logger.error("Error during sorting by time: %s", error)
        raise DateTimeConversionError from error
