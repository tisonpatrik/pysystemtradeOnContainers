"""Module to handle seeding the database asynchronously."""

import asyncio
import logging

from src.data_processing.csv_helper import load_csv
from src.db.repositories.repository import PostgresRepository
from src.db.schemas.schemas import get_schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeedDBHandler:
    """
    Initializes the SeedDBHandler with the given schemas and database repository,
    or defaults if none provided.

    Parameters:
    - schemas: List of configuration schemas to be processed.
    - repository: Repository for database operations.
    """
    def __init__(self):
        self.schemas = get_schemas()
        self.repository = PostgresRepository()

    async def insert_data_from_csv_async(self):
        """
        Asynchronously inserts data from CSV files into the database for all given schemas.

        This involves loading the data from each CSV file and inserting it into the database according to the table name
        specified in each schema.
        """
        tasks = [self._load_csv_and_insert_data_to_db_async(schema) for schema in self.schemas]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error("Error occurred while inserting data from CSV: %s", result)


    async def _load_csv_and_insert_data_to_db_async(self, schema):
        """
        Asynchronously loads data from a CSV file specified in a given schema and inserts it into the database.

        Parameters:
        - schema: The configuration schema detailing the CSV file path and target table name.
        """
        try:
            data_frame = load_csv(schema.file_path)
            await self.repository.insert_data_async(data_frame, schema.table_name)
        except Exception as error:
            logger.error("Error occurred while processing the CSV file %s: %s", schema.file_path, error)
            raise error
