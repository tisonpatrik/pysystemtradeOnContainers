import logging
from src.db.schemas.config_schemas.instrument_config_schema import InstrumentConfigSchema
from src.db.schemas.config_schemas.instrument_metadata_schema import InstrumentMetadataSchema
from src.db.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db.schemas.config_schemas.spread_cost_schema import SpreadCostSchema
from src.db.repositories.repository import PostgresRepository

import pandas as pd
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseHandler:

    DEFAULT_SCHEMAS = [
        InstrumentConfigSchema(),
        InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema()
    ]

    def __init__(self, config_schemas=None):
        """Initialize the handler with default or provided config schemas."""
        self.config_schemas = config_schemas or self.DEFAULT_SCHEMAS

    async def _process_schema_async(self, schema, repository):
        """
        Process a single schema: Read the CSV file and insert the data.
        """
        df = pd.read_csv(schema.file_path)
        await repository.insert_data_async(df, schema.table_name)

    async def insert_data_from_csv(self) -> None:
        """
        Insert data from CSV files for all schemas.
        """
        repository = PostgresRepository()
        tasks = [self._process_schema_async(schema, repository) for schema in self.schemas]
        await asyncio.gather(*tasks)

    def init_tables(self) -> None:
        """
        Initialize tables in the database using schemas.
        """
        repository = PostgresRepository()
        for schema in self.schemas:
            repository.create_table(schema.sql_command)

    def reset_tables(self) -> None:
        """
        Reset the database by dropping tables and re-initializing.
        """
        repository = PostgresRepository()
        try:
            repository.reset_db()
        except Exception as e:
            logger.error(f"Failed to reset the database: {str(e)}")
            raise e