from src.db.schemas.base_config_schema import BaseConfigSchema
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, schema: BaseConfigSchema):
        self.schema = schema

    async def load_file(self):
        df = self._load_csv()
        df = self._rename_columns_if_needed(df)
        df = self._handle_empty_values(df)
        return df

    def _load_csv(self) -> pd.DataFrame:
        """Load CSV file from the defined path."""
        try:
            logger.info(f"Loading CSV file from {self.schema.origin_csv_file_path}")
            return pd.read_csv(self.schema.origin_csv_file_path)
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def _rename_columns_if_needed(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename DataFrame columns based on schema column mapping."""
        if self.schema.column_mapping:
            df.rename(columns=self.schema.column_mapping, inplace=True)
            logger.info("Columns renamed according to provided mapping.")
        return df

    def _handle_empty_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle empty values within the DataFrame."""
        df.fillna("")
        df = df.applymap(lambda x: "" if x == "" else x)
        return df

    def process_data(self, df: pd.DataFrame):
        """Save the processed DataFrame to the defined path."""
        try:
            df.to_csv(self.schema.file_path, index=False)
            logger.info(f"Data saved to {self.schema.file_path}")
            return self.schema.file_path
        except Exception as e:
            logger.error(f"Error saving data to temp folder: {e}")
            raise
