import logging
from typing import List, Union
from src.db.schemas.schemas import get_configs_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.data_preprocessor import process_data
from src.data_processing.csv_helper import load_csv, save_to_csv

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigDataHandler:
    def __init__(self, schemas: List[BaseConfigSchema] = None):
        """
        Initializes the ConfigDataHandler with the given schemas, or defaults if none provided.
        
        Parameters:
        - schemas: List of configuration schemas to be processed.
        """
        self.schemas = schemas if schemas else get_configs_schemas()

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

    def _process_config_schema(self, schema: BaseConfigSchema) -> Union[bool, Exception]:
        """
        Processes a single configuration schema synchronously.
        This includes loading the data from the specified CSV file, transforming the data 
        according to the given schema, and then saving the transformed data back to the same CSV file.
        
        If any error occurs during processing, logs an error message with details and returns the exception.
        
        Parameters:
        - schema: The configuration schema detailing how the data should be processed.
        """
        try:
            data = load_csv(schema.origin_csv_file_path)
            data = process_data(data, schema.column_mapping)
            save_to_csv(data, schema.file_path)
            logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
            return True
        except Exception as e:
            logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")
            return e
