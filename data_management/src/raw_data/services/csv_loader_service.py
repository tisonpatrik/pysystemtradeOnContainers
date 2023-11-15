"""
Provides utilities for reading CSV files.
"""
import os

import pandas as pd

from src.core.errors.csv_read_errors import (
    CsvEmptyDataError,
    CsvFileNotFoundException,
    CsvParserError,
    CsvUnexpectedError,
)

from src.utils.logging import AppLogger


class CsvLoaderService():
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def load_csv(self,full_path) -> pd.DataFrame:
        """
        Loads a CSV file from a given path and returns it as a DataFrame.
        """
        try:
            data_frame = pd.read_csv(full_path)
            return data_frame
        except FileNotFoundError as file_not_found_exc:
            self.logger.error("File not found: %s", full_path)
            raise CsvFileNotFoundException(
                f"File not found: {full_path}"
            ) from file_not_found_exc
        except pd.errors.EmptyDataError as empty_data_exc:
            self.logger.error("No data: %s", full_path)
            raise CsvEmptyDataError(f"No data in file: {full_path}") from empty_data_exc
        except pd.errors.ParserError as parser_error_exc:
            self.logger.error("Error parsing file: %s", full_path)
            raise CsvParserError(f"Error parsing file: {full_path}") from parser_error_exc
        except Exception as unexpected_error_exc:
            self.logger.error("Unexpected error occurred: %s", unexpected_error_exc)
            raise CsvUnexpectedError(
                f"Unexpected error occurred: {unexpected_error_exc}"
            ) from unexpected_error_exc


def get_csv_files_from_directory(directory: str) -> list:
    """
    Get the list of all CSV files from the specified directory.
    """
    return [f for f in os.listdir(directory) if f.endswith(".csv")]
