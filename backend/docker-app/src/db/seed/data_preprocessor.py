from src.db.schemas.config_schemas.base_config_schema import BaseConfigSchema
import pandas as pd
import logging
import csv
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, schema: BaseConfigSchema):
        self.schema = schema

    def load_files(self) -> pd.DataFrame:
        try:
            logger.info(f"Loading CSV file from {self.schema.origin_csv_file_path}")
            df = pd.read_csv(self.schema.origin_csv_file_path)
            logger.info("CSV file loaded successfully.")
            
            if self.schema.column_mapping:
                df.rename(columns=self.schema.column_mapping, inplace=True)
                df.fillna("")
                # Replace empty cells with an empty string
                df = df.applymap(lambda x: "" if x == "" else x)
                logger.info("Columns renamed according to provided mapping.")            
            return df
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def process_data(self, df: pd.DataFrame):
        try:
            df.to_csv(self.schema.file_path, index=False)
            logger.info(f"Data saved to {self.schema.file_path}")
            return self.schema.file_path
        except Exception as e:
            logger.error(f"Error saving data to temp folder: {e}")
            raise
