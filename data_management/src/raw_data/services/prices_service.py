"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.
"""

from src.common_utils.utils.data_aggregation.data_aggregators import concatenate_data_frames
from src.raw_data.operations.prices_operations import process_single_csv_file
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.raw_data.core.errors.raw_data_processing_error import ProcessingError, PricesFilesProcessingError

from src.utils.logging import AppLogger

class PricesService:
    """
    Manages the processing and adjustment of pricing data from CSV files.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader_service = CsvLoaderService()
        
        self.date_time_column = "unix_date_time"
        self.price_column = "price"
        self.symbol_column = "symbol"

    def process_prices_files(self, model):
        """
        Process and prices for a given table mapping.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)

            csv_files_names = self.csv_loader_service.get_csv_files_from_directory(model.directory)
            processed_data_frames = self._process_csv_files(csv_files_names, model)
            price_data_frames = concatenate_data_frames(processed_data_frames)
            return price_data_frames
        
        except PricesFilesProcessingError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise


    def _process_csv_files(self, csv_files_names, model):
        """
        Processes each CSV file in the given list.
        """
        processed_data_frames = []
        for csv_file_name in csv_files_names:
            try:
                self.logger.info("Processing CSV file: %s", csv_file_name)
                processed_df = process_single_csv_file(csv_file_name, model, self.price_column, self.date_time_column, self.symbol_column)
                processed_data_frames.append(processed_df)
            except Exception as exc:
                self.logger.error("An unexpected error occurred while processing %s: %s", csv_file_name, exc)
                raise ProcessingError(f"An unexpected error occurred during processing of {csv_file_name}.") from exc
        return processed_data_frames