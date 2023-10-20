"""
Provides asynchronous utilities for reading and writing CSV files.
"""
import logging
import glob
import asyncio
from typing import List
import aiofiles

from aiocsv.readers import AsyncDictReader
from src.csv_io.schemas.csv_output import CsvOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CsvFilesService:
    """
    A class to work with CSV files asynchronously.
    """

    async def load_csv_files_from_directory_async(self, mapping) -> List[CsvOutput]:
        """
        Loads CSV files from the specified directory asynchronously.

        Args:
            path_to_directory (str): The path to the directory containing CSV files.

        Returns:
            List[CsvOutput]: A list of CsvOutput objects representing the loaded CSV files.
        """
        csv_outputs = []
        try:
            csv_files = glob.glob(f"{mapping.directory}/*.csv")
            tasks = [self.load_csv_async(csv_file) for csv_file in csv_files]
            data_list = await asyncio.gather(*tasks)

            for full_path, data in zip(csv_files, data_list):
                csv_output = CsvOutput(
                    full_path=full_path, table=mapping.table, data=data
                )
                csv_outputs.append(csv_output)

            logger.info("Successfully loaded all CSV files from %s.", mapping.directory)
        except Exception as e:
            logger.error(
                "An error occurred while loading CSV files from %s: %s",
                mapping.directory,
                e,
            )
            raise

        return csv_outputs

    async def load_csv_async(self, full_path) -> List[dict]:
        """
        Loads a CSV file asynchronously and returns a CsvOutput object.

        Args:
            full_path (str): The full path to the CSV file to be loaded.

        Returns:
            Dataframe representing the loaded CSV file.
        """
        try:
            # Log the action
            logger.info("Loading CSV file from %s", full_path)

            # Load the DataFrame asynchronously
            async with aiofiles.open(full_path, mode="r") as file:
                async_reader = AsyncDictReader(file)
                dataframe = [row async for row in async_reader]

            return dataframe

        except Exception as e:
            # Log the error
            logger.error("Error loading CSV file from %s: %s", full_path, e)
            raise
