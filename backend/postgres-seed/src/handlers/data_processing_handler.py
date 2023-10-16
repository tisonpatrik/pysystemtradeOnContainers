"""
Module to handle raw data processing.
"""

import logging

from src.data_processing.data_preprocessor import (
    process_all_csv_in_directory,
    save_concatenated_dataframes,
)
from src.db.schemas.schemas import get_data_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.handlers.errors import ProcessingError

from src.data_processing.csv_helper import load_csv_files_from_directory

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessingHandler:
    """
    Handles raw data processing tasks.
    """

    def __init__(self):
        self.schemas = get_data_schemas()

    def handle_data_processing(self) -> None:
        """
        Processes each schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """

        data = self._load_dataframes()
        

    def _process_raw_data_schema(self, schema: BaseConfigSchema):
        try:
            processed_dataframes = process_all_csv_in_directory(
                schema.origin_csv_directory_path, schema.column_mapping
            )
            if processed_dataframes:
                save_concatenated_dataframes(processed_dataframes, schema.file_path)
            else:
                logger.error(
                    "No valid data to save for schema: %s", schema.__class__.__name__
                )
        except FileNotFoundError:
            logger.error(
                "File not found while processing schema: %s", schema.__class__.__name__
            )
        except KeyError:
            logger.error(
                "KeyError occurred while processing schema: %s",
                schema.__class__.__name__,
            )
        except ValueError:
            logger.error(
                "ValueError occurred while processing schema: %s",
                schema.__class__.__name__,
            )
        except ProcessingError as error:  # Keeping a general Exception as a last resort
            logger.error(
                "An unidentified error occurred while processing the schema: %s", error
            )

    def _clean_folder_paths(self):
        """
        Cleans the list of folder paths by removing duplicates.

        Returns:
            List[str]: A list of unique folder paths.
        """
        # Use a set comprehension to eliminate duplicates
        unique_directory_paths = {
            schema.origin_csv_directory_path for schema in self.schemas
        }

        # Convert the set back to a list
        return list(unique_directory_paths)

    def _load_dataframes(self):
        """
        Loads DataFrames from directories and aggregates them into a list.

        Returns:
            List[List[pd.DataFrame]]: A list of lists of DataFrames.
        """
        # Use the cleaned list of folder paths
        paths = self._clean_folder_paths()

        # Use a list comprehension to load and aggregate DataFrames
        aggregated_dataframes = [load_csv_files_from_directory(path) for path in paths]
        return aggregated_dataframes
