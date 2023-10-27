"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
import asyncio
import os
import logging

from src.seed_raw_data.services.mapping_service import MappingService
from src.seed_raw_data.services.table_to_db_service import TableToDBService
from src.db.services.data_insert_service import DataInsertService

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
        self.data_insert_service = DataInsertService()

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """

        mapping = self.mapping_service.load_mappings_from_json()
        datas = await self.table_to_db_service.get_processed_data_from_raw_files(
            mapping
        )
        for data in datas:
            print(data.get_table_name())
        # for data in datas:
        #     await self.data_insert_service.insert_dataframe_async(data.data_frame, data.table)

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
