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
    InvalidFileNameError,
)

logger = AppLogger.get_instance().get_logger()


def load_csv(full_path) -> pd.DataFrame:
    """
    Loads a CSV file from a given path and returns it as a DataFrame.
    """
    try:
        data_frame = pd.read_csv(full_path)
        return data_frame
    except Exception as error:
        logger.error("Error loading CSV file from %s: %s", full_path, error)
        raise CsvLoadingError(full_path, str(error))


def get_full_path(directory: str, file_name: str) -> str:
    """
    Validates the full file path constructed from the provided directory and file_name.
    """
    full_path = os.path.join(directory, file_name)
    if not os.path.exists(full_path):
        raise InvalidFileNameError(f"File path {full_path} does not exist.")
    return full_path
