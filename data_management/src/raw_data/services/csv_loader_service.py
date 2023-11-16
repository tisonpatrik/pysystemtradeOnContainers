"""
Provides utilities for reading CSV files.
"""
import os
import glob

import polars as pl

from src.raw_data.core.errors.csv_loading_errors import CsvLoadingError, MultipleCsvLoadingError
from src.utils.logging import AppLogger

class CsvLoaderService():
    
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def load_csv(self, full_path):
        """
        Loads a CSV file from a given path and returns it as a DataFrame.
        """
        try:
            data_frame = pl.read_csv(full_path, infer_schema_length = 500, truncate_ragged_lines=True)
            return data_frame
        except Exception as error:
            self.logger.error("Error loading CSV file from %s: %s", full_path, error)
            raise CsvLoadingError(full_path, str(error))

    def load_multiple_csv_files(self, directory):
        """
        Loads multiple CSV files from a given directory and returns a list of DataFrames.
        """
        data_frames_dict = {}
        try:
            for filepath in glob.glob(os.path.join(directory, '*.csv')):
                symbol_name = os.path.basename(filepath).split('.')[0]
                df = self.load_csv(filepath)
                data_frames_dict[symbol_name] = df
            return data_frames_dict
        except Exception as error:
            self.logger.error("Error loading multiple CSV files from directory %s: %s", directory, error)
            raise MultipleCsvLoadingError(directory, str(error))
