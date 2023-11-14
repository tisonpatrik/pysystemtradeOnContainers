"""
Module for date-time related conversion utilities.
"""

import logging
import time

import pandas as pd

from src.core.errors.date_time_errors import (
    DateTimeConversionError,
    InvalidDatetimeColumnError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_column_to_datetime(
    data_frame: pd.DataFrame, date_time_column: str, unit=None
) -> pd.DataFrame:
    """
    Converts a specified column in the DataFrame to datetime format.
    """
    # Step 1: Copy the original DataFrame to avoid altering it
    copied_data_frame = data_frame.copy()

    # Step 2: Convert the specified column to datetime format
    try:
        converted = convert_column(copied_data_frame, date_time_column, unit)
        return converted
    except Exception as error:
        logger.error(
            "Failed to convert column %s to datetime: %s", date_time_column, error
        )
        raise InvalidDatetimeColumnError(
            f"Failed to convert {date_time_column} to datetime"
        ) from error


def convert_column(data_frame: pd.DataFrame, column_name: str, unit):
    """
    Attempts to convert a column to datetime format, dropping NAs generated by coercion.
    """
    data_frame[column_name] = pd.to_datetime(
        data_frame[column_name], errors="coerce", unit=unit
    )
    data_frame.dropna(subset=[column_name], inplace=True)
    return data_frame


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
