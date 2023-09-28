"""
Module for preprocessing CSV data.

This module provides functions for loading, preprocessing, and handling CSV data.
It enables renaming of columns, aggregation of data, and other preparatory operations
for downstream analyses.
"""

import logging
import os

from src.data_processing.csv_helper import load_csv
from src.data_processing.errors import (
    CSVFileNotFoundError,
    ColumnRenamingError,
    DataAggregationError
)
from src.data_processing.data_frame_helper import (
    add_symbol_by_file_name,
    aggregate_to_day_based_prices,
    convert_datetime_to_unixtime,
    rename_columns_if_needed,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_rename_columns(file_path, column_mapping):
    """
    Load and process the CSV data from the given path and rename the columns.
    """
    try:
        data_frame = load_csv(file_path)
        data_frame = rename_columns_if_needed(data_frame, column_mapping)
        logger.info("Successfully loaded and renamed columns for %s.", file_path)
        return data_frame
    except FileNotFoundError as exc:
        logger.error("CSV file not found: %s", file_path)
        raise CSVFileNotFoundError from exc
    except Exception as error:
        logger.error("Error processing data from %s: %s", file_path, error)
        raise ColumnRenamingError from error

def process_single_csv_file(file, file_path):
    try:
        time_column_name = file.columns[0]
        aggregated = aggregate_to_day_based_prices(file, time_column_name)
        converted = convert_datetime_to_unixtime(aggregated, time_column_name)
        data_frame = add_symbol_by_file_name(converted, file_path)
        logger.info("Successfully loaded and added symbol for %s.", file_path)
        return data_frame
    except FileNotFoundError as exc:
        logger.error("CSV file not found: %s", file_path)
        raise CSVFileNotFoundError from exc
    except Exception as error:
        logger.error("Error loading data from %s: %s", file_path, error)
        raise DataAggregationError from error

def load_all_csv_files_from_directory(directory_path):
    dataframes = []
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(directory_path, file_name)
        try:
            file = load_csv(file_path)
            data_frame = process_single_csv_file(file, file_path)
            dataframes.append(data_frame)
        except (CSVFileNotFoundError, DataAggregationError):
            continue

    return dataframes
