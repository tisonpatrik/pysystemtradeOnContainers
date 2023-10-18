"""
Provides asynchronous utilities for reading and writing CSV files.
"""
import logging
import glob
import asyncio
import aiofiles
import pandas as pd

from typing import List
from aiocsv.readers import AsyncDictReader
from src.csv_io.schemas.csv_output import CsvOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CsvFilesService:
    """
    A class to work with CSV files asynchronously.
    """
    
    async def load_csv_files_from_directory_async(self, path_to_directory) -> List[CsvOutput]:
        logger.info(f"Loading CSV files from {path_to_directory}")

        # Initialize an empty list to hold the DataFrames
        dataframes = []
        try:
            # Use glob to get all CSV files in the directory
            csv_files = glob.glob(f"{path_to_directory}/*.csv")

            # Create asynchronous tasks for each CSV file and read it into a DataFrame
            tasks = [self.load_csv_async(csv_file) for csv_file in csv_files]
            dataframes = await asyncio.gather(*tasks)
            # Log each file-loading action
            logger.info(f"Successfully loaded all CSV files from {path_to_directory} into DataFrames.")

        except Exception as error:
            logger.error(
                f"An error occurred while loading CSV files from {path_to_directory}: {error}"
            )
            raise

        return dataframes

    async def load_csv_async(self, full_path) -> CsvOutput:
        try:
            # Log the action
            logger.info(f"Loading CSV file from {full_path}")

            # Load the DataFrame asynchronously
            async with aiofiles.open(full_path, mode='r') as file:
                async_reader = AsyncDictReader(file)
                dataframe = [row async for row in async_reader]

            # Convert list of dictionaries to DataFrame
            dataframe = pd.DataFrame(dataframe)

            # Create the return object
            result = CsvOutput(full_path=full_path, dataframe=dataframe)

            return result

        except Exception as error:
            # Log the error
            logger.error(f"Error loading CSV file from {full_path}: {error}")
            raise