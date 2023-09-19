import pandas as pd
import os
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

def add_symbol_by_file_name(df: pd.DataFrame, file_path: str) -> pd.DataFrame:
    """
    Adds a 'symbol' column to the DataFrame by extracting the file name from the provided file path.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        file_path (str): Path to the file.

    Returns:
        pd.DataFrame: DataFrame with appended symbol column.
    """
    try:
        # Extract the file name (without extension) from the file path
        symbol = os.path.splitext(os.path.basename(file_path))[0]
        
        # Add the 'symbol' column to the DataFrame
        df['symbol'] = symbol
        
        logger.info(f"Successfully added symbol '{symbol}' from file path '{file_path}'.")

    except Exception as e:
        logger.error(f"Error adding symbol from file path '{file_path}': {e}")
        raise

    return df