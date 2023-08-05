import pandas as pd
import logging
import os
from typing import List, Union

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_csv_to_schema(file_path: str, symbol: str) -> pd.DataFrame:
    """Transforms a given CSV file to match the MultiplePrices schema."""
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()

    # Transforming the DATETIME column into UNIX timestamp
    df["UNIX_TIMESTAMP"] = pd.to_datetime(df["DATETIME"]).astype(int) // 10**9
    
    # Adding the SYMBOL column
    df["SYMBOL"] = symbol

    # Dropping the original DATETIME column
    df.drop(columns=["DATETIME"], inplace=True)

    # Reordering the columns to match the MultiplePrices schema
    df = df[["UNIX_TIMESTAMP", "SYMBOL", "CARRY", "CARRY_CONTRACT", "PRICE", "PRICE_CONTRACT", "FORWARD", "FORWARD_CONTRACT"]]

    return df

async def get_all_csv_files_async(directory_path: str) -> List[str]:
    """Get all CSV files from the given directory."""
    try:
        return [file for file in os.listdir(directory_path) if file.endswith(".csv")]
    except Exception as e:
        logger.error(f"Error listing files in directory {directory_path}: {e}")
        return []

async def process_csv_file_async(file_path: str) -> Union[pd.DataFrame, None]:
    """Process and transform a given CSV file."""
    symbol = os.path.basename(file_path).split(".")[0]
    logger.info(f"Processing file: {os.path.basename(file_path)}")
    transformed_data = transform_csv_to_schema(file_path, symbol)
    if transformed_data.empty:
        logger.warning(f"No data processed from {os.path.basename(file_path)}")
        return None
    logger.info(f"Number of rows processed from {os.path.basename(file_path)}: {len(transformed_data)}")
    return transformed_data
