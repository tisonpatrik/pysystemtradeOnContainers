"""
Handles the service logic for mapping various tables to the database. 
Responsible for orchestrating the flow of data from raw files to processed data in the database.
"""
from typing import List

from src.raw_data.core.errors.table_to_db_errors import InvalidFileNameError, ProcessingError
from src.raw_data.models.data_frame_container import DataFrameContainer
from src.raw_data.models.files_mapping import FileTableMapping
from src.raw_data.services.config_files_service import ConfigFilesService
from src.raw_data.services.prices_service import PricesService
from src.raw_data.services.rollcalendars_service import (
    RollCalendarsService,
)

from src.utils.logging import AppLogger

class TableToDBService:
    """
    Manages the conversion of raw data files to processed data for various services.
    Aggregates processed data and routes it to the appropriate database tables.
    """

    def __init__(self):
        self.config_files_service = ConfigFilesService()
        self.prices_service = PricesService()
        self.rollcalendars_service = RollCalendarsService()
        self.logger = AppLogger.get_instance().get_logger()

    def get_processed_data_from_raw_files(
        self, map_items: List[FileTableMapping]
    ) -> List[DataFrameContainer]:
        """
        Data processing for CSV files.
        """
        self.logger.info("Data processing for csv files has started")
        processed_data = []
        for map_item in map_items:
            try:
                result = self._process_map_item(map_item)
                if result:
                    processed_data.append(result)

            except InvalidFileNameError:
                self.logger.error(
                    "Encountered an error with file name: %s",
                    map_item.file_name,
                    exc_info=True,
                )
            except ProcessingError:
                self.logger.error(
                    "Processing failed for file: %s", map_item.file_name, exc_info=True
                )
        return processed_data

    def _process_map_item(self, map_item: FileTableMapping):
        """
        Processes individual FileTableMapping item based on its table attribute.
        """
        if map_item.table in ["instrument_config", "roll_config", "spread_cost"]:
            return self.config_files_service.process_config_files(map_item)
        if map_item.table in ["adjusted_prices", "fx_prices", "multiple_prices"]:
            return self.prices_service.process_prices_files(map_item)
        if map_item.table == "roll_calendars":
            return self.rollcalendars_service.process_roll_calendars(map_item)
        return None
