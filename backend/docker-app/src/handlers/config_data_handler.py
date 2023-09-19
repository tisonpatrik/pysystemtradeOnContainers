import logging
from typing import List
from src.db.schemas.schemas import get_configs_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.data_preprocessor import process_config_data
from src.data_processing.csv_helper import load_csv, save_to_csv
from src.db.repositories.repository import PostgresRepository 
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigDataHandler:
    def __init__(self, 
                 schemas: List[BaseConfigSchema] = None, 
                 repository: PostgresRepository = None):
        """
        Initializes the ConfigDataHandler with the given schemas and database repository, 
        or defaults if none provided.
        
        Parameters:
        - schemas: List of configuration schemas to be processed.
        - repository: Repository for database operations.
        """
        self.schemas = schemas if schemas else get_configs_schemas()
        self.repository = repository if repository else PostgresRepository()

    def handle_data_processing(self) -> None:
        """
        Processes each configuration schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """
        results = [self._process_config_schema(schema) for schema in self.schemas]

        # Log any exceptions that occurred during processing
        for schema, result in zip(self.schemas, results):
            if isinstance(result, Exception):
                logger.error(f"Error processing data for schema {schema.__class__.__name__}: {result}")

    def _process_config_schema(self, schema: BaseConfigSchema) -> None:
        """
        Processes a single configuration schema synchronously.
        This includes loading the data from the specified CSV file, transforming the data 
        according to the given schema, and then saving the transformed data back to the same CSV file.
        
        If any error occurs during processing, logs an error message with details.
        
        Parameters:
        - schema: The configuration schema detailing how the data should be processed.
        """
        try:
            data = load_csv(schema.file_path)
            data = process_config_data(data, schema.column_mapping)
            save_to_csv(data, schema.file_path)
            logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")
            raise e


    async def insert_data_from_csv_async(self) -> None:
        """
        Asynchronously inserts data from CSV files into the database for all given schemas.
        
        This involves loading the data from each CSV file and inserting it into the database according to the table name
        specified in each schema.
        """
        tasks = [self._load_csv_and_insert_data_to_db_async(schema) for schema in self.schemas]
        results = await asyncio.gather(*tasks, return_exceptions=True) # Change here to capture exceptions

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error occurred while inserting data from CSV: {result}")

    async def _load_csv_and_insert_data_to_db_async(self, schema: BaseConfigSchema) -> None:
        """
        Asynchronously loads data from a CSV file specified in a given schema and inserts it into the database.
        
        Parameters:
        - schema: The configuration schema detailing the CSV file path and target table name.
        """
        try:
            df = load_csv(schema.file_path)
            await self.repository.insert_data_async(df, schema.table_name)
        except Exception as e:
            logger.error(f"Error occurred while processing the CSV file {schema.file_path}: {e}")
            raise e  # Re-raise the exception for the gather method to capture


