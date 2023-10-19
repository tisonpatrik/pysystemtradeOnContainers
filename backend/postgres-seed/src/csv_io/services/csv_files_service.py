"""
Provides asynchronous utilities for reading and writing CSV files.
"""
import logging
import glob
import asyncio
from typing import List
import aiofiles
import pandas as pd

from aiocsv.readers import AsyncDictReader
from src.csv_io.schemas.csv_output import CsvOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CsvFilesService:
    """
    A class to work with CSV files asynchronously.
    """

    async def load_csv_files_from_directory_async(
        self, path_to_directory
    ) -> List[CsvOutput]:
        """
        Loads CSV files from the specified directory asynchronously.

        Args:
            path_to_directory (str): The path to the directory containing CSV files.

        Returns:
            List[CsvOutput]: A list of CsvOutput objects representing the loaded CSV files.
        """
        logger.info("Loading CSV files from %s", path_to_directory)

        # Initialize an empty list to hold the DataFrames
        dataframes = []
        try:
            # Use glob to get all CSV files in the directory
            csv_files = glob.glob(f"{path_to_directory}/*.csv")

            # Create asynchronous tasks for each CSV file and read it into a DataFrame
            tasks = [self.load_csv_async(csv_file) for csv_file in csv_files]
            dataframes = await asyncio.gather(*tasks)
            # Log each file-loading action
            logger.info(
                "Successfully loaded all CSV files from %s into DataFrames.",
                path_to_directory,
            )

        except Exception as e:
            logger.error(
                "An error occurred while loading CSV files from %s: %s",
                path_to_directory,
                e,
            )
            raise

        return dataframes

    async def load_csv_async(self, full_path) -> CsvOutput:
        """
        Loads a CSV file asynchronously and returns a CsvOutput object.

        Args:
            full_path (str): The full path to the CSV file to be loaded.

        Returns:
            CsvOutput: An object representing the loaded CSV file.
        """
        try:
            # Log the action
            logger.info("Loading CSV file from %s", full_path)

            # Load the DataFrame asynchronously
            async with aiofiles.open(full_path, mode="r") as file:
                async_reader = AsyncDictReader(file)
                dataframe = [row async for row in async_reader]

            # Convert list of dictionaries to DataFrame
            dataframe = pd.DataFrame(dataframe)

            # Create the return object
            result = CsvOutput(full_path=full_path, dataframe=dataframe)

            return result

        except Exception as e:
            # Log the error
            logger.error("Error loading CSV file from %s: %s", full_path, e)
            raise
