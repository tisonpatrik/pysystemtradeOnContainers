"""
Module: ConfigFilesService
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""
import logging

from src.seed_raw_data.schemas.files_mapping import FileTableMapping
from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.seed_raw_data.schemas.data_frame_container import DataFrameContainer
from src.seed_raw_data.errors.table_to_db_errors import ProcessingError
from src.data_processor.data_processing.files_helper import FilesHelper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigFilesService:
    """
    Handles the processing of configuration data.
    Reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object.
    """

    def __init__(self):
        self.csv_files_service = CsvFilesService()
        self.tables_helper = TablesHelper()
        self.files_helper = FilesHelper()

    def process_config_files(self, map_item: FileTableMapping):
        """
        Processes configuration data from a FileTableMapping object.

        Args:
            map_item (FileTableMapping): The object containing mapping information for file processing.

        Returns:
            DataFrameContainer: Encapsulated Pandas DataFrame with renamed columns and table name.
        """
        try:
            logger.info("Starting the process for %s table.", map_item.table)        
            full_path = self.files_helper.get_full_path(map_item.directory, map_item.file_name)
            raw_data = self.csv_files_service.load_csv(full_path)
            renamed = self.tables_helper.rename_columns(raw_data, map_item.columns_mapping)
            return DataFrameContainer(renamed, map_item.table)

        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            raise ProcessingError("An unexpected error occurred during processing.") from e