import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rename_columns_if_needed(df: pd.DataFrame, column_mapping: dict = None) -> pd.DataFrame:
    """Rename DataFrame columns based on the provided column mapping."""
    if column_mapping:
        df.rename(columns=column_mapping, inplace=True)
        logger.info("Columns renamed according to provided mapping.")
    return df

def handle_empty_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle empty values within the DataFrame."""
    df.fillna("", inplace=True)  # inplace=True for inplace operation
    df = df.applymap(lambda x: "" if x == "" else x)
    return df

