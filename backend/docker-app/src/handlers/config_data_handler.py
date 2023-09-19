import logging
from typing import List
from src.db.schemas.schemas import get_configs_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.config_data_preprocessor import ConfigDataPreprocessor
from src.data_processing.csv_handler import CSVHandler
from src.db.repositories.repository import PostgresRepository 
import pandas as pd
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigDataHandler:

    def __init__(self, schemas: List[BaseConfigSchema] = None):
        """Initialize the handler with injected or provided config schemas."""
        self.schemas = schemas if schemas else get_configs_schemas()

    async def handle_data_processing_async(self) -> None:
        """Process each configuration schema asynchronously."""
        for schema in self.schemas:
            await self._process_config_schema_async(schema)

    async def _process_config_schema_async(self, schema: BaseConfigSchema) -> None:
        """
        Asynchronously attempt to process a given config schema,
        log errors if any.
        """
        try:
            data = self._load_data(schema.file_path)
            data = await self._process_data(schema, data)
            await self._save_data(schema, data)
            logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")

    def _load_data(self, path: str) -> pd.DataFrame:
        csv_handler = CSVHandler()
        return csv_handler.load_csv(path)

    async def _process_data(self, schema: BaseConfigSchema, data: pd.DataFrame) -> pd.DataFrame:
        """Asynchronously load data for a given schema using DataPreprocessor."""
        preprocessor = ConfigDataPreprocessor()
        return await preprocessor.process_data_async(data, schema.column_mapping)

    async def _save_data(self, schema: BaseConfigSchema, data: pd.DataFrame) -> None:
        """Asynchronously process data for a given schema using DataPreprocessor."""
        csv_handler = CSVHandler()
        await csv_handler.save_to_csv_async(data, schema.file_path)  # Assuming this method in CSVHandler is async now.

    async def insert_data_from_csv_async(self) -> None:
        """
        Insert data from CSV files for all schemas.
        """
        repository = PostgresRepository()
        tasks = [self._load_csv_and_insert_data_async(schema, repository) for schema in self.schemas]
        await asyncio.gather(*tasks)

    async def _load_csv_and_insert_data_async(self, schema: BaseConfigSchema, repository: PostgresRepository) -> None:
        """
        Process a single schema: Read the CSV file and insert the data.
        """
        df = pd.read_csv(schema.file_path)
        await repository.insert_data_async(df, schema.table_name)  # Assuming the repository method is already async.
