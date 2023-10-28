"""
This module provides services for handling and manipulating date-time data within DataFrames.
It makes use of utility classes DateTimeHelper and TablesHelper for various data transformations.
"""
import logging
import pandas as pd

from typing import List

from src.data_processor.schemas.series_schema import SeriesSchema
from src.common_utils.utils.validators.columns_validators import (
    check_single_missing_column,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_unix_time_to_datetime,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DateTimeService:
    """
    Provides services for handling and manipulating date-time data in Pandas DataFrames.
    It makes use of DateTimeHelper for date-time conversions and TablesHelper for table manipulations.
    """

    def covert_dataframe_to_list_of_series(
        self, df: pd.DataFrame, symbol_column: str, index_column: str
    ) -> List[SeriesSchema]:
        """
        Converts the DataFrame to a list of SeriesSchema objects.
        """
        logger.info(f"Processing dataframes to series")

        series_schemas = []
        check_single_missing_column(df, symbol_column)
        check_single_missing_column(df, index_column)
        time_converted = convert_unix_time_to_datetime(df, index_column)
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
