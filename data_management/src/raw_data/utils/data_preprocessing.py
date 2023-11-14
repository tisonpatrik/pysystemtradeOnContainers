"""
This module provides utilities for preprocessing raw data files, specifically
CSV files. It performs tasks such as loading the CSV into a DataFrame, 
removing unnamed columns, renaming columns based on a mapping, and converting
specified columns to date-time format.
"""

import pandas as pd

from src.common_utils.utils.column_operations.rename_columns import (
    remove_unnamed_columns,
    rename_columns,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
)
from src.raw_data.models.files_mapping import FileTableMapping
from src.raw_data.utils.csv_loader import load_csv
from src.raw_data.utils.path_validator import get_full_path


def preprocess_raw_data(
    csv_file_name: str, map_item: FileTableMapping, date_time_column: str
) -> pd.DataFrame:
    """
    Preprocess a given raw CSV data file and returns a cleaned DataFrame.
    """
    full_path = get_full_path(map_item.directory, csv_file_name)
    raw_data = load_csv(full_path)
    removed_unnamed_columns = remove_unnamed_columns(raw_data)
    renamed_data = rename_columns(removed_unnamed_columns, map_item.columns_mapping)
    date_time_converted_data = convert_column_to_datetime(
        renamed_data, date_time_column
    )
    return date_time_converted_data
