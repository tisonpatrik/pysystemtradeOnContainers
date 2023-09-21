"""
Module to handle raw data processing.
"""

import logging
import os

import pandas as pd

from src.data_processing.csv_helper import save_to_csv
from src.data_processing.data_frame_helper import rename_columns_if_needed
from src.data_processing.data_preprocessor import load_all_csv_files_from_directory
from src.db.schemas.schemas import get_raw_data_schemas
from src.handlers.errors import ProcessingError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataHandler:
    """
    Initializes the RawDataHandler with provided schemas or defaults.

    Parameters:
    - schemas: List of raw data schemas to be processed.
    """
    def __init__(self):
        self.schemas = get_raw_data_schemas()

    def handle_data_processing(self) -> None:
        """
        Processes each configuration schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """
        results = [self._process_raw_data_schema(schema) for schema in self.schemas]

        # Log any exceptions that occurred during processing
        for schema, result in zip(self.schemas, results):
            if isinstance(result, Exception):
                logger.error(
                    "Error processing data for schema %s: %s",
                    schema.__class__.__name__,
                    result
                )

    def _process_raw_data_schema(self, schema):
        if not os.path.isdir(schema.origin_csv_file_path):
            logger.warning("Directory not found: %s", schema.origin_csv_file_path)
            return

        data_frames = load_all_csv_files_from_directory(schema.origin_csv_file_path)

        if not data_frames:
            logger.warning("No valid CSV files found in %s", schema.origin_csv_file_path)
            return

        if not self._process_and_save_dataframes(data_frames, schema):
            logger.error(
                "Failed to process and save data for schema: %s",
                schema.__class__.__name__
            )

    def _process_and_save_dataframes(self, data_frames, schema):
        """
        Concatenates and processes a list of dataframes and saves the result to a specified path.

        Parameters:
        - dataframes: List of DataFrames to be processed.
        - save_path: Path to save the processed data.

        Returns:
        - True if processing was successful, False otherwise.
        """
        try:
            concatenated_df = pd.concat(data_frames, ignore_index=True)
            # Drop columns that have 'Unnamed' in their name
            cleaned_df = concatenated_df.drop(columns=[col for col in concatenated_df.columns if "Unnamed" in col])
            renamed_df = rename_columns_if_needed(cleaned_df, schema.column_mapping)
            save_to_csv(renamed_df, schema.file_path)
            return True
        except Exception as generic_exception:
            logger.error("Error during concatenation or data processing: %s", generic_exception)
            raise ProcessingError from generic_exception
