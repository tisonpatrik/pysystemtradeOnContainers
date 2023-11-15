"""
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""

from src.raw_data.core.errors.table_to_db_errors import ProcessingError
from src.raw_data.operations.config_files_operations import process_config_files_table
from src.utils.logging import AppLogger

class ConfigFilesService:
    """
    Handles the processing of configuration data.
    """
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()


    def process_config_files(self, map_item):
        """
        Processes configuration data from a FileTableMapping object.
        """
        try:
            self.logger.info("Starting the process for %s table.", map_item.__tablename__)
            data_frame = process_config_files_table(map_item)
            return data_frame

        except Exception as exc:
            self.logger.error("An unexpected error occurred: %s", exc)
            raise ProcessingError("An unexpected error occurred during processing.") from exc
