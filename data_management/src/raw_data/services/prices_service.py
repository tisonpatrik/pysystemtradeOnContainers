"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.
"""

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from src.raw_data.operations.prices_operations import process_single_csv_file
from src.raw_data.services.csv_loader_service import CsvLoaderService

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

    def process_prices_files(self, map_item):
        """
        Process and prices for a given table mapping.
        """
        self.logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = self.csv_loader_service.get_csv_files_from_directory(map_item.directory)

        # Initialize list to store processed DataFrames
        price_data_frames = concatenate_data_frames(
            [
                process_single_csv_file(
                    csv_file_name,
                    map_item,
                    self.price_column,
                    self.date_time_column,
                    self.symbol_column,
                )
                for csv_file_name in csv_files_names
            ]
        )

        return price_data_frames
