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
from src.common_utils.utils.column_operations.rename_columns import (
    remove_unnamed_columns,
    rename_columns,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
    convert_datetime_to_unixtime,
)
from src.raw_data.schemas.files_mapping import FileTableMapping
from src.raw_data.utils.csv_loader import load_csv
from src.raw_data.utils.path_validator import get_full_path


def process_roll_calendar_file(
    csv_file_name: str,
    map_item: FileTableMapping,
    date_time_column: str,
    symbol_column: str,
) -> pd.DataFrame:
    """
    Process a single CSV file and return a processed DataFrame.
    """
    full_path = get_full_path(map_item.directory, csv_file_name)
    symbol_name = os.path.splitext(csv_file_name)[0]

    raw_data = load_csv(full_path)
    removed_unnamed_columns = remove_unnamed_columns(raw_data)
    renamed_data = rename_columns(removed_unnamed_columns, map_item.columns_mapping)
    date_time_converted_data = convert_column_to_datetime(
        renamed_data, date_time_column
    )
    unix_time_converted_data = convert_datetime_to_unixtime(
        date_time_converted_data, date_time_column
    )
    return add_column_and_populate_it_by_value(
        unix_time_converted_data, symbol_column, symbol_name
    )
