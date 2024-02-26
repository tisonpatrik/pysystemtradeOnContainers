"""
This module contains utility functions for adding and populating columns in a pandas DataFrame.
"""

from typing import List

import pandas as pd

from common.logging.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def add_column_and_populate_it_by_value(
    data_frame: pd.DataFrame, column_name: str, column_value: str
) -> pd.DataFrame:
    """
    Adds a new column to a given Pandas DataFrame and populates it with a specified value.
    """
    try:
        # Add a new column with the specified value for all rows
        data_frame[column_name] = column_value
        return data_frame
    except Exception as exc:
        error_message = f"Error during column addition {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)


def rename_columns(
    data_frame: pd.DataFrame, new_column_names: List[str]
) -> pd.DataFrame:
    """
    Renames DataFrame columns based on the provided list of new column names.
    """
    try:
        data_frame.columns = new_column_names
        return data_frame
    except Exception as exc:
        error_message = f"rror during column renaming {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)


def convert_datetime_to_unixtime(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Converts the date_column to UNIX time.
    """
    try:
        data_frame[date_time_column] = pd.to_datetime(
            data_frame[date_time_column], errors="coerce"
        )
        data_frame[date_time_column] = (
            data_frame[date_time_column].map(pd.Timestamp.timestamp).astype(int)
        )
        return data_frame
    except Exception as error:
        error_message = f"Error during unix_date_time conversion'. {error}"
        logger.error(error_message, exc_info=True)
        raise ValueError(error_message)


def convert_and_sort_by_time(data_frame: pd.DataFrame, date_time_column: str):
    data_frame[date_time_column] = pd.to_datetime(
        data_frame[date_time_column], unit="s"
    )
    data_frame = data_frame.sort_values(by=date_time_column)
    return data_frame