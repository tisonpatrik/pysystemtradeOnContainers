"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
import asyncio
import os
import logging
import traceback

from src.seed_raw_data.services.mapping_service import MappingService
from src.seed_raw_data.services.table_to_db_service import TableToDBService

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self):
        self.mapping_service = MappingService()
        self.table_to_db_service = TableToDBService()

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """

        async def run_task(map_item):
            try:
                await self.table_to_db_service.insert_data_from_csv_to_table_async(
                    map_item
                )
                logger.info(
                    "Successfully inserted data from %s to table %s",
                    map_item.directory,
                    map_item.tables,
                )

            except Exception:
                logger.error(
                    "Failed to insert data from %s to table %s",
                    map_item.directory,
                    map_item.tables,
                )
                logger.debug(traceback.format_exc())
                # Handle or re-raise the exception as needed
                raise

        mapping = self.mapping_service.load_mappings_from_json()
        tasks = [run_task(map_item) for map_item in mapping]

        await asyncio.gather(*tasks)

    async def get_count_of_mounted_files_async(self):
        """
        Asynchronously count the number of CSV files mounted in the specified paths.
        """

        async def count_csv_files_in_directory(directory):
            return sum(1 for f in os.listdir(directory) if f.endswith(".csv"))

        mapping = self.mapping_service.load_mappings_from_json()
        # Extract directory paths from validated mappings
        tasks = [count_csv_files_in_directory(item.directory) for item in mapping]
        completed = await asyncio.gather(*tasks)

        return sum(completed)
