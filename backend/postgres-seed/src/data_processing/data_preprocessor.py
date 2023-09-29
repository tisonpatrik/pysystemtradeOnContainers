"""
Module for preprocessing CSV data.

This module provides functions for loading, preprocessing, and handling CSV data.
It enables renaming of columns, aggregation of data, and other preparatory operations
for downstream analyses.
"""

import logging
import os
import pandas as pd

from src.data_processing.csv_helper import load_csv, save_to_csv
from src.data_processing.errors import (
    ProcessingError
)
from src.data_processing.data_frame_helper import (
    add_symbol_by_file_name,
    aggregate_to_day_based_prices,
    convert_datetime_to_unixtime,
    rename_columns,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_process_raw_data_csv(file_path, column_mapping, file_name):
    try:
        df = load_csv(file_path)
        df = rename_columns(df, column_mapping)
        # Check if 'price' column is present before aggregation
        if 'price' in df.columns:
            df = aggregate_to_day_based_prices(df)

        df = convert_datetime_to_unixtime(df)
        df = add_symbol_by_file_name(df, file_name)
        return df
    except ProcessingError as e:
        logger.error(f"Error processing {file_path}: {e}")
        return None

    
def process_all_csv_in_directory(directory_path, column_mapping):
    processed_dfs = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            processed_df = load_and_process_raw_data_csv(file_path, column_mapping, os.path.splitext(file_name)[0])
            if processed_df is not None:
                processed_dfs.append(processed_df)
    return processed_dfs

def save_concatenated_dataframes(data_frames, save_path):
    concatenated_df = pd.concat(data_frames, ignore_index=True)
    drop_unnamed_column(concatenated_df)
    save_to_csv(concatenated_df, save_path)

def drop_unnamed_column(df):
    """
    Drops the column 'Unnamed: 4' from the DataFrame if it exists.
    """
    if 'Unnamed: 4' in df.columns:
        df.drop('Unnamed: 4', axis=1, inplace=True)
    return df
 