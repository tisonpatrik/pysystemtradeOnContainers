"""
Purpose: This module defines the ConfigFilesService class which processes instrument configuration data.
It reads raw CSV files, renames columns, and encapsulates the data into a DataFrameContainer object for further usage.
"""

from typing import List

import pandas as pd
from src.core.utils.logging import AppLogger
from src.data_seeder.data_processors.config_files_processor import process_config_files
from src.data_seeder.errors.config_files_errors import ConfigFilesServiceError
from src.data_seeder.utils.csv_loader import get_full_path, load_csv


class ConfigFilesSeedService:
    """
    Handles the processing of configuration data.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def process_config_files(
        self, list_of_symbols: List[str], config, column_names: List[str]
    ) -> pd.DataFrame:
        """
        Processes configuration data from a model object.
        """
        try:
            self.logger.info("Starting the process for %s table.", config.tablename)
            full_path = get_full_path(config.directory, config.file_name)
            raw_data = load_csv(full_path)
            return process_config_files(
                list_of_symbols=list_of_symbols,
                raw_data=raw_data,
                column_names=column_names,
            )
        except Exception as e:
            raise ConfigFilesServiceError(
                f"Error seeding config files for {config.tablename}: {str(e)}"
            )
