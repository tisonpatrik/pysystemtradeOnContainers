"""
Provides utilities for reading CSV files.
"""
import logging
import os

import pandas as pd

from src.raw_data.errors.csv_read_errors import (
    CsvEmptyDataError,
    CsvFileNotFoundException,
    CsvParserError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv(full_path) -> pd.DataFrame:
    """
    Loads a CSV file and returns a dataframe object.

    Args:
        full_path (str): The full path to the CSV file to be loaded.

    Returns:
        Dataframe representing the loaded CSV file.
    """
    try:
        df = pd.read_csv(full_path)
        return df
    except FileNotFoundError:
        logger.error("File not found: %s", full_path)
        raise CsvFileNotFoundException(f"File not found: {full_path}")
    except pd.errors.EmptyDataError:
        logger.error("No data: %s", full_path)
        raise CsvEmptyDataError(f"No data in file: {full_path}")
    except pd.errors.ParserError:
        logger.error("Error parsing file: %s", full_path)
        raise CsvParserError(f"Error parsing file: {full_path}")
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e)
        raise Exception(f"Unexpected error occurred: {e}")


def get_csv_files_from_directory(directory: str) -> list:
    """
    Get the list of all CSV files from the specified directory.
    """
    return [f for f in os.listdir(directory) if f.endswith(".csv")]
