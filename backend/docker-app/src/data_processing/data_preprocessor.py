from src.data_processing.data_frame_helper import rename_columns_if_needed, handle_empty_values
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_config_data(df: pd.DataFrame, column_mapping: dict = None) -> pd.DataFrame:
    """
    Process the given DataFrame by renaming columns and handling empty values.
    
    Args:
        df (pd.DataFrame): Input data.
        column_mapping (dict, optional): Mapping for renaming columns.

    Returns:
        pd.DataFrame: Processed data.
    """
    try:
        df = rename_columns_if_needed(df, column_mapping)
        df = handle_empty_values(df)
        logger.info("Processed data successfully.")
        return df

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
