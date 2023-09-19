from src.data_processing.data_frame_transformer import DataFrameTransformer
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigDataPreprocessor:

    async def process_data_async(df: pd.DataFrame, column_mapping: dict = None) -> pd.DataFrame:
        try:
            df_transformer = DataFrameTransformer(column_mapping=column_mapping)
            
            df = df_transformer.rename_columns_if_needed(df)
            df = df_transformer.handle_empty_values(df)
            
            logger.info("Processed data successfully.")
            return df
        
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise
