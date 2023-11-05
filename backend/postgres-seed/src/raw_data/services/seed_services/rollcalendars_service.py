"""
Handles processing and manipulation of roll calendar data from CSV files.
"""
import logging

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from src.raw_data.operations.rollcalendars_operations import process_roll_calendar_file
from src.raw_data.models.data_frame_container import DataFrameContainer
from src.raw_data.models.files_mapping import FileTableMapping
from src.raw_data.utils.csv_loader import get_csv_files_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RollCalendarsService:
    """
    Manages the processing of roll calendar data from CSV files.
    """

    def __init__(self):
        self.date_time_column = "unix_date_time"
        self.symbol_column = "symbol"

    def process_roll_calendars(self, map_item: FileTableMapping) -> DataFrameContainer:
        """
        Process and prices for a given table mapping.
        """
        logger.info("Starting the process for %s table.", map_item.table)

        # Get list of CSV file names in the directory
        csv_files_names = get_csv_files_from_directory(map_item.directory)

        # Initialize list to store processed DataFrames
        roll_calendars = concatenate_data_frames(
            [
                process_roll_calendar_file(
                    csv_file_name, map_item, self.date_time_column, self.symbol_column
                )
                for csv_file_name in csv_files_names
            ]
        )

        return DataFrameContainer(roll_calendars, map_item.table)