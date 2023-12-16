"""
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.data_processors.config_files_processor import ConfigFilesProcessor
from src.data_seeder.errors.config_files_errors import ConfigFilesServiceError
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.data_seeder.utils.path_validator import get_full_path
from src.db.services.data_insert_service import DataInsertService


class ConfigFilesSeedService:
    """
    Handles the processing of configuration data.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()
        self.data_insert_service = DataInsertService(db_session)
        self.config_files_processor = ConfigFilesProcessor()

    async def seed_config_files(self, list_of_symbols, model):
        """
        Processes configuration data from a model object.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.tablename)
            full_path = get_full_path(model.directory, model.file_name)
            raw_data = self.csv_loader.load_csv(full_path)
            data = self.config_files_processor.process_config_files(
                list_of_symbols=list_of_symbols, model=model, raw_data=raw_data
            )
            await self.data_insert_service.async_insert_dataframe_to_table(
                data, model.tablename
            )
        except Exception as e:
            raise ConfigFilesServiceError(
                f"Error seeding config files for {model.tablename}: {str(e)}"
            )
