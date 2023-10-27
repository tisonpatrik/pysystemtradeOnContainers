"""
Module for handling table-related operations in Pandas DataFrames.
"""

import logging
import pandas as pd
from typing import Dict
from src.data_processor.errors.table_helper_errors import (
    ColumnRenameError,
    MissingColumnsError,
    SymbolAdditionError,
    ColumnRoundingError,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TablesHelper:
    """
    Provides utility methods for column manipulation and validation in Pandas DataFrames.
    """

    def rename_columns(
        self, data_frame: pd.DataFrame, new_column_names: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Renames DataFrame columns based on the provided dictionary.
        """
        self.check_missing_columns(data_frame, new_column_names)
        self.check_for_none_values(new_column_names)
        try:
            return data_frame.rename(columns=new_column_names)
        except Exception as error:
            logger.error("Error during column renaming: %s", error)
            raise ColumnRenameError from error

    def check_missing_columns(
        self, data_frame: pd.DataFrame, new_column_names: Dict[str, str]
    ):
        """
        Checks for missing columns in the data frame.
        """
        for column in new_column_names.keys():
            self.check_single_missing_column(data_frame, column)

    def check_single_missing_column(self, data_frame: pd.DataFrame, column: str):
        """
        Checks for a single missing column in the data frame.
        """
        if column not in data_frame.columns:
            logger.error("Column '%s' does not exist in the DataFrame", column)
            raise MissingColumnsError(f"Column {column} does not exist")

    def check_for_none_values(self, new_column_names: Dict[str, str]):
        """
        Checks for None values in the new column names.
        """
        for old_name, new_name in new_column_names.items():
            if new_name is None:
                logger.error("New column name cannot be None for %s", old_name)
                raise ColumnRenameError(
                    f"New column name cannot be None for {old_name}"
                )

    def round_values_in_column(
        self, data_frame: pd.DataFrame, column_to_round: str
    ) -> pd.DataFrame:
        """
        Rounds the values in a specific column of a Pandas DataFrame.
        """
        try:
            self.check_single_missing_column(data_frame, column_to_round)
            data_frame[column_to_round] = data_frame[column_to_round].round(1)
        except Exception as error:
            logger.error("An unexpected error occurred: %s", error)
            raise ColumnRoundingError(
                f"Error rounding column '{column_to_round}'"
            ) from error

        return data_frame

    def add_column_and_populate_it_by_value(
        self, data_frame: pd.DataFrame, column_name: str, column_value: str
    ) -> pd.DataFrame:
        """
        Adds a new column to a given pandas DataFrame and populates it with a specified value.
        """
        try:
            data_frame[column_name] = column_value
            return data_frame
        except Exception as error:
            logger.error("Error during symbol addition: %s", error)
            raise SymbolAdditionError from error

    def convert_datetime_column_to_series(
        self, data_frames: pd.DataFrame, column_name: str
    ) -> pd.Series:
        """
        Converts a datetime column in a DataFrame to a Pandas Series.
        """
        try:
            self.check_single_missing_column(data_frames, column_name)
            series_result = pd.Series(index=data_frames[column_name])
            return series_result
        except Exception as e:
            logger.error(
                "Failed to convert column '%s' to series. Error: %s", column_name, e
            )
            raise RuntimeError(
                f"Failed to convert column '{column_name}' to series. Error: {e}"
            )
