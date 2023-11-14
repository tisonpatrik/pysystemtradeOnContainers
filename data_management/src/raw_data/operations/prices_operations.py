"""
This module contains operations related to processing price data from CSV files.
It provides functionalities for reading the file, renaming columns, converting date-time formats, 
aggregating data, and other related tasks to prepare a DataFrame.
"""
import os

import pandas as pd

from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)
from src.common_utils.utils.column_operations.round_column_numbers import (
    round_values_in_column,
)
from src.common_utils.utils.data_aggregation.data_aggregators import (
    aggregate_to_day_based_prices,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_datetime_to_unixtime,
)
from src.raw_data.models.files_mapping import FileTableMapping
from src.raw_data.operations.data_preprocessing import preprocess_raw_data


def process_single_csv_file(
    csv_file_name: str,
    map_item: FileTableMapping,
    price_column: str,
    date_time_column: str,
    symbol_column: str,
) -> pd.DataFrame:
    """
    Process a single CSV file and return a processed DataFrame.
    """
    symbol_name = os.path.splitext(csv_file_name)[0]
    preprocessed_data = preprocess_raw_data(csv_file_name, map_item, date_time_column)
    aggregated_data = aggregate_to_day_based_prices(preprocessed_data, date_time_column)
    unix_time_converted_data = convert_datetime_to_unixtime(
        aggregated_data, date_time_column
    )
    rounded_data = round_values_in_column(unix_time_converted_data, price_column)
    return add_column_and_populate_it_by_value(rounded_data, symbol_column, symbol_name)
