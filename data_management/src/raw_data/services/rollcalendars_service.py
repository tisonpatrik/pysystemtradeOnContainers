"""
Handles processing and manipulation of roll calendar data from CSV files.
"""
from src.raw_data.utils.data_aggregators import (
    concatenate_data_frames,
)
from src.raw_data.operations.rollcalendars_operations import process_roll_calendar_file
from src.raw_data.services.csv_loader_service import CsvLoaderService

from src.utils.logging import AppLogger

class RollCalendarsService:
    """
    Manages the processing of roll calendar data from CSV files.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader_service = CsvLoaderService()
        self.date_time_column = "unix_date_time"
        self.symbol_column = "symbol"

    def process_roll_calendars(self, map_item):
        """
        Process and prices for a given table mapping.
        """
        self.logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = self.csv_loader_service.get_csv_files_names_from_directory(map_item.directory)

        # Initialize list to store processed DataFrames
        roll_calendars = concatenate_data_frames(
            [
                process_roll_calendar_file(
                    csv_file_name, map_item, self.date_time_column, self.symbol_column
                )
                for csv_file_name in csv_files_names
            ]
        )

        return roll_calendars
