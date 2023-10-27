"""
Handles the service logic for mapping various tables to the database. 
Responsible for orchestrating the flow of data from raw files to processed data in the database.
"""
import logging
import asyncio
from typing import List
from src.seed_raw_data.schemas.data_frame_container import DataFrameContainer
from src.seed_raw_data.errors.table_to_db_errors import (
    InvalidFileNameError,
    ProcessingError,
)
from src.data_processor.services.config_files_service import ConfigFilesService
from src.data_processor.services.prices_service import PricesService
from src.data_processor.services.rollcalendars_service import RollCalendarsService
from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableToDBService:
    """
    Manages the conversion of raw data files to processed data for various services.
    Aggregates processed data and routes it to the appropriate database tables.
    """

    def __init__(self):
        self.config_files_service = ConfigFilesService()
        self.prices_service = PricesService()
        self.rollcalendars_service = RollCalendarsService()

    async def get_processed_data_from_raw_files(
        self, map_items: List[FileTableMapping]
    ) -> List[DataFrameContainer]:
        """
        Orchestrates the processing of raw data files and their conversion to database-friendly formats.
        Iterates over a list of FileTableMapping items and processes each according to its file_name attribute.
        """
        logger.info("Data processing for csv files has started")

        async def process_map_item_async(map_item):  # Define inner async function
            try:
                return await self._process_map_item(map_item)
            except (InvalidFileNameError, ProcessingError, Exception) as e:
                logger.exception(
                    f"An error occurred while processing {map_item.file_name}: {e}"
                )

        # Using asyncio.gather to run the tasks concurrently
        processed_data = await asyncio.gather(
            *[process_map_item_async(map_item) for map_item in map_items]
        )

        # Filter out None results, if any
        return [data for data in processed_data if data is not None]

    async def _process_map_item(self, map_item: FileTableMapping):
        """
        Processes individual FileTableMapping item based on its table attribute.

        Args:
            map_item (FileTableMapping): The object containing mapping information for file processing.

        Returns:
            DataFrameContainer: Processed data for the table or None if not applicable.
        """
        if map_item.table in ["instrument_config", "roll_config", "spread_cost"]:
            return self.config_files_service.process_config_files(map_item)
        elif map_item.table in ["adjusted_prices", "fx_prices", "multiple_prices"]:
            return self.prices_service.process_adjusted_prices(map_item)
        elif map_item.table == "roll_calendars":
            return self.rollcalendars_service.process_roll_calendars(map_item)
        else:
            return None
