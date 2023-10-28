"""
Provides asynchronous handler for counting CSV files in specified directories.
"""
import asyncio
import logging
import os

from src.raw_data.services.mapping_service import MappingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CsvFilesHandler:
    """
    Handles asynchronous counting of CSV files in directories specified in mappings.
    """

    def __init__(self):
        self.mapping_service = MappingService()

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
