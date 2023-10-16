"""
CSV Helper module.

This module provides utility functions for loading and saving data to CSV files. 
It contains functions `load_csv` to load data from a CSV file into a DataFrame and `save_to_csv` 
to save a DataFrame to a CSV file. A private utility function `_get_full_path` is used internally 
to get the full path to a file by combining the base and provided paths.
"""

import logging
import os
import glob

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv_files_from_directory(path_to_directory:str):
    logger.info(f"Loading CSV files from {path_to_directory}")

    # Initialize an empty list to hold the DataFrames
    dataframes = []    
    try:
        # Use glob to get all CSV files in the directory
        csv_files = glob.glob(f"{path_to_directory}/*.csv")
        
        # Loop through each CSV file and read it into a DataFrame
        for csv_file in csv_files:
            data = load_csv(csv_file)
            dataframes.append(data)
            
            # Log each file-loading action
            logger.info(f"Successfully loaded {csv_file} into a DataFrame.")
    
    except Exception as error:
        logger.error(f"An error occurred while loading CSV files from {path_to_directory}: {error}")
        raise
    
    return dataframes

def load_csv(full_path: str):
    """
    Load a CSV file from the given full path and returns an object containing the file name (without extension)
    and the loaded DataFrame.

    Args:
        full_path (str): Full path to the CSV file.

    Returns:
        dict: A dictionary containing 'file_name' and 'dataframe'.
    """
    try:
        # Log the action
        logger.info(f"Loading CSV file from {full_path}")

        # Load the DataFrame
        dataframe = pd.read_csv(full_path)

        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(full_path))[0]

        # Create the return object
        result = {
            'file_name': file_name,
            'dataframe': dataframe
        }

        return result

    except Exception as error:
        # Log the error
        logger.error(f"Error loading CSV file from {full_path}: {error}")
        raise

def save_to_csv(data_frame: pd.DataFrame, path: str, base_path: str = ""):
    """Save dataframe to the given CSV path.

    Args:
        data_frame (pd.DataFrame): Dataframe to save.
        path (str): Path to save the CSV file to.
        base_path (str): Base path for the CSV file.
    """
    full_path = _get_full_path(base_path, path)
    try:
        data_frame.to_csv(full_path, index=False)
        logger.info("Data saved to %s", full_path)
    except Exception as error:
        logger.error("Error saving data to %s: %s", full_path, error)
        raise

def _get_full_path(base_path: str, path: str) -> str:
    """Get the full path to a file, combining base and provided path."""
    return base_path + "/" + path
