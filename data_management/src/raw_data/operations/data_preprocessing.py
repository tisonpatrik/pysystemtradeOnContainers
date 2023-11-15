"""
This module provides utilities for preprocessing raw data files, specifically
CSV files. It performs tasks such as loading the CSV into a DataFrame, 
removing unnamed columns, renaming columns based on a mapping, and converting
specified columns to date-time format.
"""

from src.raw_data.utils.rename_columns import (
    remove_unnamed_columns,
    rename_columns,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
)
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.raw_data.utils.path_validator import get_full_path

def preprocess_raw_data(
    csv_file_name: str, map_item, date_time_column: str):
    """
    Preprocess a given raw CSV data file and returns a cleaned DataFrame.
    """
    full_path = get_full_path(map_item.directory, csv_file_name)
    raw_data = CsvLoaderService.load_csv(full_path)
    removed_unnamed_columns = remove_unnamed_columns(raw_data)
    column_names = [column.name for column in map_item.__table__.columns]
    renamed_data = rename_columns(removed_unnamed_columns, column_names)
    date_time_converted_data = convert_column_to_datetime(renamed_data, date_time_column)
    return date_time_converted_data
