"""
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""
import logging

from src.raw_data.errors.table_to_db_errors import ProcessingError
from src.raw_data.operations.config_files_operations import process_config_files_table
from src.raw_data.schemas.data_frame_container import DataFrameContainer
from src.raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigFilesService:
    """
    Handles the processing of configuration data.
    """

    def process_config_files(self, map_item: FileTableMapping):
        """
        Processes configuration data from a FileTableMapping object.
        """
        try:
            logger.info("Starting the process for %s table.", map_item.table)
            data_frame = process_config_files_table(map_item)
            return DataFrameContainer(data_frame, map_item.table)

        except Exception as exc:
            logger.error("An unexpected error occurred: %s", exc)
            raise ProcessingError(
                "An unexpected error occurred during processing."
            ) from exc
