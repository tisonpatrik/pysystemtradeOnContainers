"""
Module for handling table-related operations in Pandas DataFrames.
"""

import logging
import pandas as pd
from src.data_processor.errors.table_helper_errors import (
    SymbolAdditionError,
    ColumnRoundingError,
)
from src.common_utils.utils.columns_validators import check_single_missing_column

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TablesHelper:
    """
    Provides utility methods for column manipulation and validation in Pandas DataFrames.
    """

    def round_values_in_column(
        self, data_frame: pd.DataFrame, column_to_round: str
    ) -> pd.DataFrame:
        """
        Rounds the values in a specific column of a Pandas DataFrame.
        """
        try:
            check_single_missing_column(data_frame, column_to_round)
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

    def convert_dataframe_to_series(
        self, data_frames: pd.DataFrame, column_name: str
    ) -> pd.Series:
        """
        Converts a datetime column in a DataFrame to a Pandas Series.
        """
        try:
            check_single_missing_column(data_frames, column_name)
            series_result = pd.Series(index=data_frames[column_name])
            return series_result
        except Exception as e:
            logger.error(
                "Failed to convert column '%s' to series. Error: %s", column_name, e
            )
            raise RuntimeError(
                f"Failed to convert column '{column_name}' to series. Error: {e}"
            )
