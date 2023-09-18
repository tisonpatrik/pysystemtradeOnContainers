import logging
from src.db.schemas.data_schemas.multiple_prices_schema import MultiplePricesSchema
from src.db.seed.data_preprocessor import DataPreprocessor
from src.db.repositories.repository import PostgresRepository 

import pandas as pd
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataHandler:

    def __init__(self, data_schemas=None):        
        if data_schemas is None:
            # Default schemas if none provided
            self.data_schemas = [
                MultiplePricesSchema(),
            ]
        else:
            self.data_schemas = data_schemas

    def handle_data_processing(self):       
        for schema in self.config_schemas:
            try:
                self._process_config_schema(schema)
                logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")
                # You can choose to raise the exception or continue with the next schema
                continue

    def _process_config_schema(self, schema):
        preprocessor = DataPreprocessor(schema)
        data = preprocessor.load_file()  # Assuming visibility of load_files is public
        preprocessor.process_data(data)

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
