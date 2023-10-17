"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
import asyncio
import os
import logging

from src.configs.raw_data import settings
from src.handlers.errors import DatabaseError

from sqlalchemy.ext.asyncio import AsyncSession

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedDBHandler:
    """
    This class provides methods to seed the database asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """

    async def get_count_of_mounted_files_async(self):
        """
        Asynchronously count the number of CSV files mounted in the specified paths in the settings.
        """
        mapping = settings.file_to_table_mapping
        counts = {}

        async def count_csv_files_in_directory(directory):
            return sum(1 for f in os.listdir(directory) if f.endswith(".csv"))

        tasks = []
        for key, path in mapping.items():
            tasks.append(asyncio.ensure_future(count_csv_files_in_directory(path)))

        completed, _ = await asyncio.gather(*tasks)

        for idx, (key, _) in enumerate(mapping.items()):
            counts[key] = completed[idx]

        return counts
