"""
Provides utilities for reading CSV files.
"""

import os

import pandas as pd

from common.logging.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def load_csv(full_path) -> pd.DataFrame:
    """
    Loads a CSV file from a given path and returns it as a DataFrame.
    """
    try:
        data_frame = pd.read_csv(full_path)
        return data_frame
    except Exception as error:
        logger.error(f"Error loading CSV file from {full_path}: {error}")
        raise IOError(f"Error loading CSV file from {full_path}: {error}")


def get_full_path(directory: str, file_name: str) -> str:
    """
    Validates the full file path constructed from the provided directory and file_name.
    """
    full_path = os.path.join(directory, file_name)
    if not os.path.exists(full_path):
        raise ValueError(f"File path {full_path} does not exist.")
    return full_path
