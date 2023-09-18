from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.csv_handler import CSVHandler
from src.data_processing.data_frame_transformer import DataFrameTransformer
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataPreprocessor:
    def __init__(self, schema: BaseConfigSchema):
        self.schema = schema
        self.csv_handler = CSVHandler()
        self.df_transformer = DataFrameTransformer(column_mapping=self.schema.column_mapping)

    async def load_file(self):
        df = self.csv_handler.load_csv(self.schema.origin_csv_file_path)
        df = self.df_transformer.rename_columns_if_needed(df)
        df = self.df_transformer.handle_empty_values(df)
        return df

    def process_data(self, df: pd.DataFrame):
        """Save the processed DataFrame to the defined path."""
        try:
            self.csv_handler.save_to_csv(df, self.schema.file_path)
            logger.info(f"Data saved to {self.schema.file_path}")
            return self.schema.file_path
        except Exception as e:
            logger.error(f"Error saving data to temp folder: {e}")
            raise
