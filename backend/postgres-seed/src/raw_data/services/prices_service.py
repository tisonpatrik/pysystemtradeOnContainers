"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.
"""
import os
import logging
import pandas as pd

from src.raw_data.schemas.files_mapping import FileTableMapping
from src.raw_data.utils.path_validator import get_full_path
from src.raw_data.utils.csv_loader import load_csv, get_csv_files_from_directory
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.raw_data.schemas.data_frame_container import DataFrameContainer
from src.data_processor.services.date_time_service import DateTimeService
from src.common_utils.utils.rename_columns import rename_columns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PricesService:
    """
    Manages the processing and adjustment of pricing data from CSV files.
    """

    def __init__(self):
        self.tables_helper = TablesHelper()
        self.date_time_service = DateTimeService()
        self.date_time_column = "unix_date_time"
        self.price_column = "price"
        self.symbol_column = "symbol"

    def process_adjusted_prices(self, map_item: FileTableMapping) -> DataFrameContainer:
        """
        Process and prices for a given table mapping.
        """
        logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = get_csv_files_from_directory(map_item.directory)

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
        full_path = get_full_path(map_item.directory, csv_file_name)
        symbol_name = os.path.splitext(csv_file_name)[0]

        raw_data = load_csv(full_path)
        removed_unnamed_columns = raw_data.loc[
            :, ~raw_data.columns.str.contains("^Unnamed")
        ]
        renamed_data = rename_columns(removed_unnamed_columns, map_item.columns_mapping)
        aggregated_data = (
            self.date_time_service.aggregate_string_datetime_column_to_day_based_prices(
                renamed_data, self.date_time_column
            )
        )
        rounded_data = self.tables_helper.round_values_in_column(
            aggregated_data, self.price_column
        )

        return self.tables_helper.add_column_and_populate_it_by_value(
            rounded_data, self.symbol_column, symbol_name
        )
