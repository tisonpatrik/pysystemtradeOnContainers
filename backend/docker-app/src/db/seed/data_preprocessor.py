from src.db.schemas.config_schemas.base_config_schema import BaseConfigSchema
import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, schema: BaseConfigSchema):
        self.schema = schema

    def _load_files(self) -> pd.DataFrame:
        try:
            logger.info(f"Loading CSV file from {self.schema.origin_csv_file_path}")
            df = pd.read_csv(self.schema.origin_csv_file_path)
            logger.info("CSV file loaded successfully.")
            
            if self.schema.column_mapping:
                df.rename(columns=self.schema.column_mapping, inplace=True)
                logger.info("Columns renamed according to provided mapping.")
            
            return df
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def process_data(self, df: pd.DataFrame):
        try:
            temp_file_path = os.path.join(self.schema.temp_folder, f"{self.schema.table_name}.csv")
            df.to_csv(temp_file_path, index=False)
            logger.info(f"Data saved to {temp_file_path}")
            return temp_file_path
        except Exception as e:
            logger.error(f"Error saving data to temp folder: {e}")
            raise
