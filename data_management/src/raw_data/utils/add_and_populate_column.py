"""
This module contains utility functions for adding and populating columns in a pandas DataFrame.
"""
import pandas as pd
from src.core.utils.logging import AppLogger
from src.raw_data.errors.add_and_populate_error import SymbolAdditionError

logger = AppLogger.get_instance().get_logger()


def add_column_and_populate_it_by_value(
    data_frame: pd.DataFrame, column_name: str, column_value: str
) -> pd.DataFrame:
    """
    Adds a new column to a given Pandas DataFrame and populates it with a specified value.
    """
    try:
        # Add a new column with the specified value for all rows
        data_frame[column_name] = column_value
        return data_frame
    except Exception as error:
        logger.error("Error during symbol addition: %s", error)
        raise SymbolAdditionError from error
