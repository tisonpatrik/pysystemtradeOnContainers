"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.

Classes:
    - PricesService: Handles the core logic for adjusting pricing data.
"""
import os
import logging
import pandas as pd

from src.seed_raw_data.schemas.files_mapping import FileTableMapping
from src.data_processor.data_processing.file_path_validator import FilePathValidator
from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.data_processor.data_processing.date_time_helper import DateTimeHelper
from src.seed_raw_data.schemas.data_frame_container import DataFrameContainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PricesService:
    """
    Manages the processing and adjustment of pricing data from CSV files.

    Attributes:
        csv_files_service : Service for CSV loading.
        file_path_validator : Validates file paths.
        tables_helper : Assists in table manipulations.
        date_time_helper : Handles date-time conversions.
        date_time_column : Column name for date-time.
        price_column : Column name for price.

    Usage:
        prices_service = PricesService()
        df_container = prices_service.process_adjusted_prices(map_item)
    """

    def __init__(self):
        self.csv_files_service = CsvFilesService()
        self.file_path_validator = FilePathValidator()
        self.tables_helper = TablesHelper()
        self.date_time_helper = DateTimeHelper()
        self.date_time_column = "unix_date_time"
        self.price_column = "price"

    def process_adjusted_prices(self, map_item: FileTableMapping) -> DataFrameContainer:
        """
        Process and prices for a given table mapping.
        """
        logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = self._get_csv_files_from_directory(map_item.directory)

        # Initialize list to store processed DataFrames
        processed_data_frames = []

        # Process each CSV file
        for csv_file_name in csv_files_names:
            processed_df = self._process_single_csv_file(csv_file_name, map_item)
            processed_data_frames.append(processed_df)

        # Concatenate all processed DataFrames into a single DataFrame
        concatenated_data_frame = pd.concat(processed_data_frames, ignore_index=True)

        return DataFrameContainer(concatenated_data_frame, map_item.table)

    def _process_single_csv_file(
        self, csv_file_name: str, map_item: FileTableMapping
    ) -> pd.DataFrame:
        """
        Process a single CSV file and return a processed DataFrame.
        """
        full_path = self.file_path_validator.get_full_path(
            map_item.directory, csv_file_name
        )
        symbol_name = os.path.splitext(csv_file_name)[0]

        raw_data = self.csv_files_service.load_csv(full_path)
        renamed_data = self.tables_helper.rename_columns(
            raw_data, map_item.columns_mapping
        )
        date_time_converted_data = self.date_time_helper.convert_column_to_datetime(
            renamed_data, self.date_time_column
        )
        aggregated_data = self.date_time_helper.aggregate_to_day_based_prices(
            date_time_converted_data, self.date_time_column
        )
        unix_time_converted_data = self.date_time_helper.convert_datetime_to_unixtime(
            aggregated_data, self.date_time_column
        )
        rounded_data = self.tables_helper.round_values_in_column(
            unix_time_converted_data, self.price_column
        )

        return self.tables_helper.add_column_and_populate_it_by_value(
            rounded_data, "symbol", symbol_name
        )

    def _get_csv_files_from_directory(self, directory: str) -> list:
        """
        Get the list of all CSV files from the specified directory.
        """
        return [f for f in os.listdir(directory) if f.endswith(".csv")]
