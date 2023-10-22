"""
bla
"""

import logging
import pandas as pd
from typing import Dict
from src.data_processor.errors.data_processing_errors import ColumnRenameError, MissingColumnsError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TablesHelper:

    def rename_columns(self, data_frame: pd.DataFrame, new_column_names: Dict[str, str]) -> pd.DataFrame:
            """
            Renames DataFrame columns based on the provided dictionary.
            """
            self._check_missing_columns(data_frame, new_column_names)
            self._check_for_none_values(new_column_names)
            try:
                return data_frame.rename(columns=new_column_names)
            except Exception as error:
                logger.error("Error during column renaming: %s", error)
                raise ColumnRenameError from error
        
    def _check_missing_columns(self, data_frame: pd.DataFrame, new_column_names: Dict[str, str]):
            """
            Checks for missing columns in the data frame.
            """
            missing_columns = set(new_column_names.keys()) - set(data_frame.columns)
            if missing_columns:
                missing_columns_str = ", ".join(missing_columns)
                logger.error("Columns %s do not exist in the DataFrame", missing_columns_str)
                raise MissingColumnsError(f"Columns {missing_columns_str} do not exist")
            
    def _check_for_none_values(self, new_column_names: Dict[str, str]):
            """
            Checks for None values in the new column names.
            """
            for old_name, new_name in new_column_names.items():
                if new_name is None:
                    logger.error("New column name cannot be None for %s", old_name)
                    raise ColumnRenameError(f"New column name cannot be None for {old_name}")