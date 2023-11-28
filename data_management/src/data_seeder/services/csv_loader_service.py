"""
Provides utilities for reading CSV files.
"""
import glob
import os
from typing import List

import polars as pl
from src.core.utils.logging import AppLogger
from src.data_seeder.errors.csv_loading_errors import (
    CsvLoadingError,
    MultipleCsvLoadingError,
)


class CsvLoaderService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def load_csv(self, full_path):
        """
        Loads a CSV file from a given path and returns it as a DataFrame.
        """
        try:
            data_frame = pl.read_csv(
                full_path, infer_schema_length=500, truncate_ragged_lines=True
            )
            return data_frame
        except Exception as error:
            self.logger.error("Error loading CSV file from %s: %s", full_path, error)
            raise CsvLoadingError(full_path, str(error))

    def load_multiple_csv_files(self, directory: str, list_of_symbols: List[str]):
        """
        Loads multiple CSV files from a given directory and returns a list of DataFrames.
        """
        data_frames_dict = {}
        try:
            for filepath in glob.glob(os.path.join(directory, "*.csv")):
                symbol_name = os.path.splitext(os.path.basename(filepath))[0]
                if symbol_name in list_of_symbols:
                    df = self.load_csv(filepath)
                    data_frames_dict[symbol_name] = df
            return data_frames_dict
        except Exception as error:
            self.logger.error(
                "Error loading multiple CSV files from directory %s: %s",
                directory,
                error,
            )
            raise MultipleCsvLoadingError(directory, str(error))

    def get_csv_file_names_for_directory(self, directory):
        """
        Returns a list of names of all .csv files in the specified directory, without the extension.
        """
        try:
            csv_files = glob.glob(os.path.join(directory, "*.csv"))
            file_names = [
                os.path.splitext(os.path.basename(file))[0] for file in csv_files
            ]
            return file_names
        except Exception as error:
            self.logger.error(
                f"Error retrieving CSV file names from directory {directory}: {error}"
            )
            raise CsvLoadingError(directory, str(error))