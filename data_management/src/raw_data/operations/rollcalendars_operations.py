"""
This module is responsible for handling operations related to roll calendars.
It provides functionalities for reading CSV files, renaming columns, converting date-time data, 
and performing other relevant data transformations.
"""
import os

import pandas as pd

from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_datetime_to_unixtime,
)
from src.raw_data.services.raw_data_service import RawFilesService


def process_roll_calendar_file(
    csv_file_name: str,
    map_item,
    date_time_column: str,
    symbol_column: str,
) -> pd.DataFrame:
    """
    Process a single CSV file and return a processed DataFrame.
    """
    symbol_name = os.path.splitext(csv_file_name)[0]
    preprocessed_data = RawFilesService.preprocess_raw_data(csv_file_name, map_item, date_time_column)
    unix_time_converted_data = convert_datetime_to_unixtime(
        preprocessed_data, date_time_column
    )
    return add_column_and_populate_it_by_value(
        unix_time_converted_data, symbol_column, symbol_name
    )
