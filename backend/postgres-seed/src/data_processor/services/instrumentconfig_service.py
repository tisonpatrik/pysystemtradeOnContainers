"""
Module: InstrumentConfigService
Purpose: This module defines the InstrumentConfigService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""
import os
import logging

from src.seed_raw_data.schemas.files_mapping import FileTableMapping
from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.seed_raw_data.schemas.data_frame_container import DataFrameContainer
from src.seed_raw_data.errors.table_to_db_errors import ProcessingError, InvalidFileNameError
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstrumentConfigService:
    """
    Handles the processing of instrument configuration data.
    Reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object.
    """

    def __init__(self):
        self.csv_files_service = CsvFilesService()
        self.tables_helper = TablesHelper()

    def process_instrument_config(self, map_item: FileTableMapping):
        """
        Processes instrument configuration data from a FileTableMapping object.

        Args:
            map_item (FileTableMapping): The object containing mapping information for file processing.

        Returns:
            DataFrameContainer: Encapsulated Pandas DataFrame with renamed columns and table name.
        """
        try:
            logger.info("Starting the process for instrument_config table.")
            
            full_path = self._get_full_path(map_item)
            
            raw_data = self.csv_files_service.load_csv(full_path)
            renamed = self.tables_helper.rename_columns(raw_data, map_item.columns_mapping)
            return DataFrameContainer(renamed, map_item.table)

        except InvalidFileNameError as e:
            logger.error("Invalid file name error: %s", e)
            raise e

        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            raise ProcessingError("An unexpected error occurred during processing.") from e

    def _get_full_path(self, map_item: FileTableMapping):
        """
        Validates the file path based on the provided FileTableMapping object.

        Args:
            map_item (FileTableMapping): The object containing mapping information for file processing.

        Returns:
            str: The full file path if valid.

        Raises:
            InvalidFileNameError: If the file path is invalid or does not exist.
        """
        full_path = os.path.join(map_item.directory, map_item.file_name)
        if not os.path.exists(full_path):
            raise InvalidFileNameError(f"File path {full_path} does not exist.")
        return full_path