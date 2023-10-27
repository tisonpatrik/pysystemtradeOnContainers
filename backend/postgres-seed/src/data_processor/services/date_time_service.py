"""
bla bla
"""
import logging
import pandas as pd
from backend.shared import src

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.data_processor.data_processing.date_time_helper import DateTimeHelper
from src.data_processor.data_processing.tables_helper import TablesHelper


class DateTimeService:
    """
    bla bla
    """

    def __init__(self):
        self.date_time_helper = DateTimeHelper()
        self.tables_helper = TablesHelper()

    def convert_string_column_to_unixtime(
        self, data_frame: pd.DataFrame, date_time_column: str
    ) -> pd.DataFrame:
        """
        bla bla
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
        bla bla
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
        bla bla
        """
        date_time_frame = self.date_time_helper.convert_unix_time_to_datetime(
            data_frame, date_time_column
        )
        series = self.tables_helper.convert_datetime_column_to_series(
            date_time_frame, date_time_column
        )
        return series
