import os
import logging
from typing import List
import pandas as pd

from src.data_processing.data_frame_helper import (
    rename_columns_if_needed,
    handle_empty_values,
    add_symbol_by_file_name
)
from src.data_processing.csv_helper import load_csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rename_columns_and_handle_empty_values(file_path: str, column_mapping: dict = None) -> pd.DataFrame:
    """
    Load and process the CSV data from a given path by renaming columns and handling empty values.
    
    Args:
        origin_csv_file_path (str): Path to the source CSV file.
        column_mapping (dict, optional): Mapping for renaming columns.

    Returns:
        pd.DataFrame: Processed data.
    """
    try:
        df = load_csv(file_path)
        df = rename_columns_if_needed(df, column_mapping)
        df = handle_empty_values(df)
        logger.info(f"Successfully processed data from {file_path}.")
        return df

    except Exception as e:
        logger.error(f"Error processing data from {file_path}: {e}")
        raise

def load_all_csv_files_from_directory(directory_path: str) -> List[pd.DataFrame]:
    """
    Loads all CSV files from a directory, extracts the symbol from the filename, 
    and appends it to each dataframe.

    Args:
        directory_path (str): Path to the directory containing the CSV files.

    Returns:
        List[pd.DataFrame]: List of DataFrames with appended symbol columns.
    """
    dataframes = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            try:
                df = load_csv(file_path)
                dataframes.append(add_symbol_by_file_name(df, file_path))
                logger.info(f"Successfully loaded and added symbol for {file_path}.")
            except Exception as e:
                logger.error(f"Error loading data from {file_path}: {e}")

    return dataframes
