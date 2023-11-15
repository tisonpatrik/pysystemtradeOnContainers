"""
Provides utilities for reading CSV files.
"""
import os
import polars as pl
from src.utils.logging import AppLogger

class CsvLoaderService():
    
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def load_csv(self,full_path) -> pl.DataFrame:
        """
        Loads a CSV file from a given path and returns it as a DataFrame.
        """
        data_frame = pl.read_csv(full_path)
        return data_frame


    def get_csv_files_from_directory(directory: str) -> list:
        """
        Get the list of all CSV files from the specified directory.
        """
        return [f for f in os.listdir(directory) if f.endswith(".csv")]
