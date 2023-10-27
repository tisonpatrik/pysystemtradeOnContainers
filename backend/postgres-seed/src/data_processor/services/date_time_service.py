"""
This module provides services for handling and manipulating date-time data within DataFrames.
It makes use of utility classes DateTimeHelper and TablesHelper for various data transformations.
"""
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.data_processor.data_processing.date_time_helper import DateTimeHelper
from src.data_processor.data_processing.tables_helper import TablesHelper


class DateTimeService:
    """
    Provides services for handling and manipulating date-time data in Pandas DataFrames.
    It makes use of DateTimeHelper for date-time conversions and TablesHelper for table manipulations.
    """

    def __init__(self):
        self.date_time_helper = DateTimeHelper()
        self.tables_helper = TablesHelper()

    def convert_string_column_to_unixtime(
        self, data_frame: pd.DataFrame, date_time_column: str
    ) -> pd.DataFrame:
        """
        Converts a column in a DataFrame containing date-time strings to UNIX time format.
        """

        date_time_converted_data = self.date_time_helper.convert_column_to_datetime(
            data_frame, date_time_column
        )
        unix_time_converted_data = self.date_time_helper.convert_datetime_to_unixtime(
            date_time_converted_data, date_time_column
        )
        return unix_time_converted_data

    def aggregate_string_datetime_column_to_day_based_prices(
        self, data_frame: pd.DataFrame, date_time_column: str
    ) -> pd.DataFrame:
        """
        Aggregates the data in a DataFrame's date-time column to daily frequency.
        """

        date_time_converted_data = self.date_time_helper.convert_column_to_datetime(
            data_frame, date_time_column
        )
        unix_time_converted_data = self.date_time_helper.convert_datetime_to_unixtime(
            date_time_converted_data, date_time_column
        )
        aggregated_data = self.date_time_helper.aggregate_to_day_based_prices(
            unix_time_converted_data, date_time_column
        )
        return aggregated_data

    def convert_raw_dataframe_to_series(
        self, data_frame: pd.DataFrame, date_time_column: str
    ) -> pd.Series:
        """
        Converts a column with raw date-time data in a DataFrame into a Pandas Series.
        """
        date_time_frame = self.date_time_helper.convert_unix_time_to_datetime(
            data_frame, date_time_column
        )
        series = self.tables_helper.convert_datetime_column_to_series(
            date_time_frame, date_time_column
        )
        return series
