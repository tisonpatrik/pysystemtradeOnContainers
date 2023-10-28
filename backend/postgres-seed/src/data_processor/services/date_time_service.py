"""
This module provides services for handling and manipulating date-time data within DataFrames.
It makes use of utility classes DateTimeHelper and TablesHelper for various data transformations.
"""
import logging
import pandas as pd

from typing import List

from src.data_processor.data_processing.date_time_helper import DateTimeHelper
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.data_processor.schemas.series_schema import SeriesSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def covert_dataframe_to_list_of_series(
        self, df: pd.DataFrame, symbol_column: str, index_column: str
    ) -> List[SeriesSchema]:
        """
        Converts the DataFrame to a list of SeriesSchema objects.
        """
        logger.info(f"Processing dataframes to series")

        series_schemas = []
        self.tables_helper.check_single_missing_column(df, symbol_column)
        self.tables_helper.check_single_missing_column(df, index_column)
        time_converted = self.date_time_helper.convert_unix_time_to_datetime(
            df, index_column
        )
        try:
            grouped = time_converted.groupby(symbol_column)

            for group in grouped:
                # Getting the symbol from the first item of the group
                first_item = group[1].iloc[0]
                symbol_value = first_item[symbol_column]

                group_dropped = group[1].drop(columns=[symbol_column])
                series = group_dropped.set_index(index_column).squeeze()

                schema = SeriesSchema(symbol_value, series)
                series_schemas.append(schema)

        except Exception as e:
            logger.error(
                "An error occurred while converting DataFrame to SeriesSchemas: %s", e
            )
            raise
        return series_schemas
