"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

import logging

from src.handlers.errors import DatabaseError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import asyncio

from src.data_processing.csv_helper import load_csv
from src.db.repositories.data_inserter import DataInserter
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.db.schemas.schemas import get_data_schemas


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

    async def get_available_seed_files_names_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """

    #     tasks = [
    #         self._load_csv_and_insert_data_to_db_async(schema)
    #         for schema in self.schemas
    #     ]
    #     results = await asyncio.gather(*tasks, return_exceptions=True)

    #     for result in results:
    #         if isinstance(result, Exception):
    #             logger.error("Error occurred while inserting data from CSV: %s", result)

    # async def _load_csv_and_insert_data_to_db_async(self, schema: BaseConfigSchema):
    #     """
    #     Asynchronously load data from a CSV file and insert it into the database as specified by the schema.
    #     """
    #     data_seeder = DataInserter(self.database_url)
    #     try:
    #         # Using the refactored load_csv_file_and_filename method
    #         loaded_data = load_csv(schema.file_path)

    #         # Extract DataFrame and file name from the returned dictionary
    #         data_frame = loaded_data["dataframe"]
    #         file_name = loaded_data["file_name"]

    #         # Log the action
    #         logger.info(f"Processing CSV file: {file_name}")

    #         # Insert the DataFrame into the database
    #         await data_seeder.insert_dataframe_async(data_frame, schema.table_name)

    #     except Exception as error:
    #         logger.error(
    #             f"Error occurred while processing the CSV file {schema.file_path}: {error}"
    #         )
    #         raise error
