import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFrameTransformer:

    def __init__(self, column_mapping: dict = None):
        self.column_mapping = column_mapping

    def rename_columns_if_needed(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename DataFrame columns based on the provided column mapping."""
        if self.column_mapping:
            df.rename(columns=self.column_mapping, inplace=True)
            logger.info("Columns renamed according to provided mapping.")
        return df

    def handle_empty_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle empty values within the DataFrame."""
        df.fillna("", inplace=True)  # inplace=True for inplace operation
        df = df.applymap(lambda x: "" if x == "" else x)
        return df
