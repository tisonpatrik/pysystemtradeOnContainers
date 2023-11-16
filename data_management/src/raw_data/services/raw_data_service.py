"""
This module provides utilities for preprocessing raw data files, specifically
CSV files. It performs tasks such as loading the CSV into a DataFrame, 
removing unnamed columns, renaming columns based on a mapping, and converting
specified columns to date-time format.
"""

from src.raw_data.utils.rename_columns import rename_columns
from src.raw_data.utils.date_time_convertions import convert_string_column_to_datetime
from src.raw_data.core.errors.raw_data_processing_error import ConfigFilesProcessingError
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.utils.logging import AppLogger

class RawFilesService:
    """
    Handles the processing of raw data.
    """
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()

    def preprocess_raw_data(self, dataframe, model, symbol_name):
        """
        Preprocess a given raw CSV data file and returns a cleaned DataFrame.
        """
        try:
            column_names = [column.name for column in model.__table__.columns if column.name != model.symbol.name]
            renamed_data = rename_columns(dataframe, column_names)
            date_time_converted_data = convert_string_column_to_datetime(renamed_data, model.unix_date_time.name)
            return date_time_converted_data
        except Exception as exc:
            self.logger.error(f"Error preprocessing CSV file {symbol_name}: {exc}")
            raise ConfigFilesProcessingError("An unexpected error occurred during processing.") from exc
