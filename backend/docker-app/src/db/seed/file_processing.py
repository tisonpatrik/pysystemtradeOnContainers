import pandas as pd
import logging
import os
from typing import List, Union, Dict

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_csv_to_schema_general(file_path: str, symbol: str, column_mapping: Dict[str, str]) -> Union[pd.DataFrame, None]:
    """Transforms a given CSV file to a general schema based on column mapping."""
    try:
        df = pd.read_csv(file_path)
        datetime_col = "DATETIME" if "DATETIME" in df.columns else "DATE_TIME"
        df["UNIX_TIMESTAMP"] = pd.to_datetime(df[datetime_col]).astype(int) // 10**9
        df["SYMBOL"] = symbol
        df.drop(columns=[datetime_col], inplace=True)
        for csv_col, schema_col in column_mapping.items():
            df.rename(columns={csv_col: schema_col}, inplace=True)
        desired_columns = ["UNIX_TIMESTAMP", "SYMBOL"] + list(column_mapping.values())
        df = df[desired_columns]
        return df
    except Exception as e:
        logger.error(f"Error processing CSV file {file_path}: {e}")
        return None

async def get_all_csv_files_async(directory_path: str) -> List[str]:
    """Get all CSV files from the given directory."""
    try:
        return [file for file in os.listdir(directory_path) if file.endswith(".csv")]
    except Exception as e:
        logger.error(f"Error listing files in directory {directory_path}: {e}")
        return []

async def process_csv_file_async(file_path: str, column_mapping: Dict[str, str]) -> Union[pd.DataFrame, None]:
    """Process and transform a given CSV file."""
    symbol = os.path.basename(file_path).split(".")[0]
    logger.info(f"Processing file: {os.path.basename(file_path)}")
    transformed_data = transform_csv_to_schema_general(file_path, symbol, column_mapping)
    if transformed_data is None or transformed_data.empty:
        logger.warning(f"No data processed from {os.path.basename(file_path)}")
        return None
    logger.info(f"Number of rows processed from {os.path.basename(file_path)}: {len(transformed_data)}")
    return transformed_data