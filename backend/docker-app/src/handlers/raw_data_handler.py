import logging
import os
import pandas as pd
from typing import List
from src.db.schemas.schemas import get_raw_data_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.data_preprocessor import process_data
from src.data_processing.csv_helper import load_csv, save_to_csv

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataHandler:
    def __init__(self, schemas: List[BaseConfigSchema] = None):
        """
        Initializes the RawDataHandler with the given schemas, or defaults if none provided.
        
        Parameters:
        - schemas: List of configuration schemas to be processed.
        """
        self.schemas = schemas if schemas else get_raw_data_schemas()

    def handle_data_processing(self) -> None:
        for schema in self.schemas:
            self._process_config_schema(schema)

    def _process_config_schema(self, schema: BaseConfigSchema) -> None:
        dataframes = []
        
        # Iterate over all CSV files in the folder
        for file_name in os.listdir(schema.origin_csv_file_path):
            if file_name.endswith('.csv'):
                # Load the CSV file
                file_path = os.path.join(schema.origin_csv_file_path, file_name)
                df = load_csv(file_path)
                
                # Add "symbol" column
                symbol = os.path.splitext(file_name)[0]  # Remove the .csv extension to get the symbol
                df['symbol'] = symbol
                
                dataframes.append(df)
        
        # Concatenate all dataframes into one
        df = pd.concat(dataframes, ignore_index=True)
        
        df = process_data(df)
        save_to_csv(df, schema.file_path)
