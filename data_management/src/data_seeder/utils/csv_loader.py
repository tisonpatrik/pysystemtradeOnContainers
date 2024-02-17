"""
Provides utilities for reading CSV files.
"""

import glob
import os
from typing import List

import pandas as pd
from src.core.utils.logging import AppLogger
from src.data_seeder.errors.csv_loading_errors import (
    CsvLoadingError,
    MultipleCsvLoadingError,
)
from src.data_seeder.errors.path_validation_error import InvalidFileNameError

logger = AppLogger.get_instance().get_logger()


def load_csv(full_path):
    """
    Loads a CSV file from a given path and returns it as a DataFrame.
    """
    try:
        data_frame = pd.read_csv(full_path)
        return data_frame
    except Exception as error:
        logger.error("Error loading CSV file from %s: %s", full_path, error)
        raise CsvLoadingError(full_path, str(error))


def load_multiple_csv_files(
    directory: str, list_of_symbols: List[str], ignore_symbols: bool = False
):
    """
    Loads multiple CSV files from a given directory and returns a list of DataFrames.
    Optionally ignores symbol filtering based on the 'ignore_symbols' flag.
    """
    data_frames_dict = {}
    try:
        for filepath in glob.glob(os.path.join(directory, "*.csv")):
            symbol_name = os.path.splitext(os.path.basename(filepath))[0]

            # Load CSV if ignore_symbols is True or symbol is in list_of_symbols
            if ignore_symbols or symbol_name in list_of_symbols:
                df = load_csv(filepath)
                data_frames_dict[symbol_name] = df

        return data_frames_dict
    except Exception as error:
        logger.error(
            "Error loading multiple CSV files from directory %s: %s",
            directory,
            error,
        )
        raise MultipleCsvLoadingError(directory, str(error))


def get_csv_file_names_for_directory(directory):
    """
    Returns a list of names of all .csv files in the specified directory, without the extension.
    """
    try:
        csv_files = glob.glob(os.path.join(directory, "*.csv"))
        file_names = [os.path.splitext(os.path.basename(file))[0] for file in csv_files]
        return file_names
    except Exception as error:
        logger.error(
            f"Error retrieving CSV file names from directory {directory}: {error}"
        )
        raise CsvLoadingError(directory, str(error))


def get_full_path(directory: str, file_name: str) -> str:
    """
    Validates the full file path constructed from the provided directory and file_name.
    """
    full_path = os.path.join(directory, file_name)
    if not os.path.exists(full_path):
        raise InvalidFileNameError(f"File path {full_path} does not exist.")
    return full_path
