import logging
from src.db.schemas.schemas import get_raw_data_schemas

import pandas as pd
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataHandler:

    def __init__(self, schemas: list = None):
        """Initialize the handler with injected or provided config schemas."""
        self.schemas = schemas if schemas else get_raw_data_schemas()

    async def handle_data_processing(self):
        """Process each configuration schema asynchronously."""
        for schema in self.schemas:
            await self._try_process_config_schema(schema)

    async def _try_process_config_schema(self, schema):
        """
        Asynchronously attempt to process a given config schema, log errors if any.
        """
        try:
            data = await self._load_data_for_schema(schema)
            await self._process_data_for_schema(schema, data)
            logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")

    async def _load_data_for_schema(self, schema):
        """Asynchronously load data for a given schema using DataPreprocessor."""


    async def insert_data_from_csv(self) -> None:
        """
        Insert data from CSV files for all schemas.
        """
