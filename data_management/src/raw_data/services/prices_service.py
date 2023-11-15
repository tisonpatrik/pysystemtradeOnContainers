"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.
"""
import logging

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from src.raw_data.operations.prices_operations import process_single_csv_file
from src.core.utils.csv_loader import get_csv_files_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PricesService:
    """
    Manages the processing and adjustment of pricing data from CSV files.
    """

    def __init__(self):
        self.date_time_column = "unix_date_time"
        self.price_column = "price"
        self.symbol_column = "symbol"

    def process_prices_files(self, map_item):
        """
        Process and prices for a given table mapping.
        """
        logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = get_csv_files_from_directory(map_item.directory)

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
