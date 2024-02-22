"""
Module for date-time related conversion utilities.
"""

import pandas as pd

from common.logging.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


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
