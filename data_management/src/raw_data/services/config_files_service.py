"""
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""

from src.raw_data.core.errors.raw_data_processing_error import ConfigFilesProcessingError
from src.raw_data.utils.rename_columns import rename_columns
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.raw_data.utils.path_validator import get_full_path
from src.utils.logging import AppLogger

class ConfigFilesService:
    """
    Handles the processing of configuration data.
    """
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()

    def process_config_files(self, model):
        """
        Processes configuration data from a FileTableMapping object.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)
            full_path = get_full_path(model.directory, model.file_name)
            raw_data = self.csv_loader.load_csv(full_path)
            column_names = [column.name for column in model.__table__.columns]
            renamed_data = rename_columns(raw_data, column_names)
            return renamed_data

        except Exception as exc:
            self.logger.error("An unexpected error occurred: %s", exc)
            raise ConfigFilesProcessingError("An unexpected error occurred during processing.") from exc
