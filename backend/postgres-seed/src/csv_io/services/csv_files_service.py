"""
Provides asynchronous utilities for reading and writing CSV files.
"""
import logging
import glob
import asyncio
from typing import List
import aiofiles
import pandas as pd
import os

from aiocsv.readers import AsyncDictReader
from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CsvFilesService:
    """
    A class to work with CSV files asynchronously.
    """

    async def load_csv_files_from_directory_async(
        self, mapping: FileTableMapping
    ) -> List[pd.DataFrame]:
        """
        Asynchronously loads CSV files from a directory into Pandas DataFrames.

        Args:
            mapping (FileTableMapping): Object specifying directory and other CSV details.

        Returns:
            List[pd.DataFrame]: A list of Pandas DataFrames representing the loaded CSV files.
        """
        dataframes = []
        try:
            csv_files_path = self._prepare_path(
                mapping.multiple_files, mapping.directory, mapping.file_name
            )
            tasks = [
                self.load_csv_async(csv_file) for csv_file in csv_files_path
            ]  # load_csv_async loads raw CSV data
            raw_csv_data_list = await asyncio.gather(*tasks)
            for raw_csv_data in raw_csv_data_list:
                # Assuming raw_csv_data is a string; adjust as needed
                df = pd.read_csv(raw_csv_data)
                dataframes.append(df)

            logger.info(
                "Successfully loaded all CSV files from %s into Pandas DataFrames.",
                mapping.directory,
            )
        except Exception as e:
            logger.error(
                "An error occurred while loading CSV files from %s into Pandas DataFrames: %s",
                mapping.directory,
                e,
            )
            raise

        return dataframes

    def _prepare_path(self, multiple_files: bool, directory: str, file_name: str):
        csv_files = None
        if multiple_files:
            csv_files = glob.glob(f"{directory}/*.csv")
        else:
            csv_files = [f"{directory}/{file_name}.csv"]
        return csv_files

    async def load_csv_async(self, full_path) -> List[dict]:
        """
        Loads a CSV file asynchronously and returns a dataframe object.

        Args:
            full_path (str): The full path to the CSV file to be loaded.

        Returns:
            Dataframe representing the loaded CSV file.
        """
        try:
            # Load the DataFrame asynchronously
            async with aiofiles.open(full_path, mode="r") as file:
                async_reader = AsyncDictReader(file)
                dataframe = [row async for row in async_reader]

            return dataframe

        except Exception as e:
            # Log the error
            logger.error("Error loading CSV file from %s: %s", full_path, e)
            raise
