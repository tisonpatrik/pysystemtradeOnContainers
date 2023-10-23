"""
Module for preprocessing CSV data.

This module provides functions for loading, preprocessing, and handling CSV data.
It enables renaming of columns, aggregation of data, and other preparatory operations
for downstream analyses.
"""

import logging
import os

from src.data_processing.csv_helper import load_csv, save_to_csv
from src.data_processing.data_frame_helper import (
    add_column_and_populate_it_by_value,
    aggregate_to_day_based_prices,
    concat_dataframes,
    convert_datetime_to_unixtime,
    rename_columns,
)
from src.data_processing.errors import ProcessingError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_process_raw_data_csv(file_path, column_mapping):
    """
    Loads and processes raw data from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
        column_mapping (dict): A mapping from old column names to new column names.
        file_name (str): The name of the file, used to add a 'symbol' column.

    Returns:
        pd.DataFrame or None: A DataFrame containing the processed data, or None if an error occurs.
    """
    try:
        data_frame = load_csv(file_path)
        data_frame = data_frame["dataframe"]
        file_name = data_frame["file_name"]
        data_frame = rename_columns(data_frame, column_mapping)
        # Check if 'price' column is present before aggregation
        if "price" in data_frame.columns:
            data_frame = aggregate_to_day_based_prices(data_frame)

        data_frame = convert_datetime_to_unixtime(data_frame)
        data_frame = add_column_and_populate_it_by_value(
            data_frame, column_name=file_name, column_value="symbol"
        )
        return data_frame
    except ProcessingError as error:  # Renamed 'e' to 'error'
        logger.error(
            "Error processing %s: %s", file_path, error
        )  # Changed to lazy formatting
        return None


def process_all_csv_in_directory(directory_path, column_mapping):
    """
    Processes all CSV files in a given directory.

    Parameters:
        directory_path (str): The path to the directory containing CSV files.
        column_mapping (dict): A mapping from old column names to new column names.

    Returns:
        list: A list of processed DataFrames.
    """
    processed_dfs = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)
            processed_df = load_and_process_raw_data_csv(
                file_path, column_mapping, os.path.splitext(file_name)[0]
            )
            if processed_df is not None:
                processed_dfs.append(processed_df)
    return processed_dfs


def save_concatenated_dataframes(data_frames, save_path):
    """
    Concatenates a list of DataFrames and saves the result to a CSV file.

    Parameters:
        data_frames (list): A list of DataFrames to concatenate.
        save_path (str): The path to save the concatenated DataFrame.
    """
    try:
        # Check if data_frames list is empty or None
        if not data_frames:
            raise ValueError("The list of DataFrames should not be empty or None.")

        # Concatenate dataframes
        try:
            concatenated_df = concat_dataframes(data_frames)
        except Exception as e:
            raise Exception(f"Failed to concatenate DataFrames: {e}")

        # Check if concatenated_df is empty
        if concatenated_df.empty:
            raise ValueError("The concatenated DataFrame is empty.")

        # Drop unnamed columns
        try:
            drop_unnamed_column(concatenated_df)
        except Exception as e:
            raise Exception(f"Failed to drop unnamed columns: {e}")

        # Save to CSV
        try:
            save_to_csv(concatenated_df, save_path)
        except Exception as e:
            raise Exception(f"Failed to save DataFrame to CSV: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def drop_unnamed_column(data_frame):
    """
    Drops the column 'Unnamed: 4' from the DataFrame if it exists.
    """
    df = data_frame
    if "Unnamed: 4" in data_frame.columns:
        df = data_frame.drop("Unnamed: 4", axis=1)
    return df
