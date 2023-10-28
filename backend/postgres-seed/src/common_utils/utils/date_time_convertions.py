import time
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.common_utils.errors.date_time_errors import (
    InvalidDatetimeColumnError,
    DateTimeConversionError,
)


def convert_column_to_datetime(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Converts a specified column in the DataFrame to datetime format.
    """
    new_df = data_frame.copy()  # Create a new DataFrame
    try:
        # Ensure the column is of a datetime type
        new_df[date_time_column] = pd.to_datetime(
            new_df[date_time_column], errors="coerce"
        )
        # Check for any NA/NaN values in the column
        if new_df[date_time_column].isna().any():
            raise InvalidDatetimeColumnError(
                f"Failed to convert all values in '{date_time_column}' to datetime."
            )
    except Exception as exc:
        logger.error(
            "Error converting column '%s' to datetime: %s",
            date_time_column,
            str(exc),
        )
        raise
    return new_df


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


def convert_unix_time_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Converts a column in a DataFrame from Unix time to datetime format.
    """
    try:
        df[column_name] = pd.to_datetime(df[column_name], unit="s")
    except Exception as e:
        logger.error(
            "Failed to convert Unix time to datetime for column '%s'. Error: %s",
            column_name,
            e,
        )
        raise RuntimeError(
            f"Failed to convert Unix time to datetime for column '{column_name}'. Error: {e}"
        )
    return df
