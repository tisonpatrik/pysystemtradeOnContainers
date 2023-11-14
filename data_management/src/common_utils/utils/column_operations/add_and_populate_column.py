"""
This module contains utility functions for adding and populating columns in a pandas DataFrame.
"""

import logging

import pandas as pd

from src.core.errors.add_and_populate_error import SymbolAdditionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_column_and_populate_it_by_value(
    data_frame: pd.DataFrame, column_name: str, column_value: str
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
