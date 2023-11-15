"""
Provides utilities for reading CSV files.
"""
import os
import polars as pl

from src.raw_data.core.errors.csv_loading_errors import CsvLoadingError
from src.utils.logging import AppLogger

class CsvLoaderService():
    
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def load_csv(self, full_path):
        """
        Loads a CSV file from a given path and returns it as a DataFrame.
        """
        try:
            self.logger.info(f"Loading CSV file from: {full_path}")
            data_frame = pl.read_csv(full_path, infer_schema_length = 500)
            return data_frame
        except Exception as error:
            self.logger.error("Error loading CSV file from %s: %s", full_path, error)
            raise CsvLoadingError(full_path, str(error))


    def get_csv_files_from_directory(self, directory: str) -> list:
        """
        Get the list of all CSV files from the specified directory.
        """
        return [f for f in os.listdir(directory) if f.endswith(".csv")]
