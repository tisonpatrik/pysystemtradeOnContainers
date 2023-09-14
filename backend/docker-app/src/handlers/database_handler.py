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

    def __init__(self, schemas=None, ):
        if schemas is None:
            # Default schemas if none provided
            self.schemas = [
                InstrumentConfigSchema(),
                InstrumentMetadataSchema(),
                RollConfigSchema(),
                SpreadCostSchema()
            ]
        else:
            self.schemas = schemas

    async def insert_data_from_csv(self) -> None:
        repository = PostgresRepository()

        async def process_schema_async(schema):
            # Load CSV file
            df = pd.read_csv(schema.file_path)

            # Insert data asynchronously
            await repository.insert_data_async(df, schema.table_name)

        # Process each schema asynchronously
        tasks = [process_schema_async(schema) for schema in self.schemas]
        await asyncio.gather(*tasks)

    
    def init_tables(self)-> None:
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
            logging.error(f"Failed to reset the database: {str(e)}")
            raise e 