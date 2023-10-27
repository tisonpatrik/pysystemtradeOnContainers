"""
bla
"""

import logging
import time

import pandas as pd

from src.data_processor.errors.date_time_errors import (
    DataAggregationError,
    InvalidDatetimeColumnError,
    DateTimeConversionError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DateTimeHelper:
    """
    bla
    """

    def aggregate_to_day_based_prices(
        self, data_frame: pd.DataFrame, date_time_column: str
    ) -> pd.DataFrame:
        """
        Aggregates the time-based price data to daily averages.
        """
        try:
            # Set DATETIME as index
            series = data_frame.set_index(date_time_column)
            # Resample to daily frequency using the mean of the prices for each day
            result = series.resample("D").mean().dropna().reset_index()
            return result
        except Exception as error:
            logger.error("Error during data aggregation: %s", error)
            raise DataAggregationError from error

    def convert_column_to_datetime(
        self, data_frame: pd.DataFrame, date_time_column: str
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
        self, data_frame: pd.DataFrame, date_time_column: str
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

    def convert_unix_time_to_datetime(
        self, df: pd.DataFrame, column_name: str
    ) -> pd.DataFrame:
        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame.")

        # Convert Unix time to datetime
        df[column_name] = pd.to_datetime(df[column_name], unit="s")

        return df
