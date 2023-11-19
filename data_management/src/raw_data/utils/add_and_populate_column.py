"""
This module contains utility functions for adding and populating columns in a pandas DataFrame.
"""
import polars as pl

from src.raw_data.errors.add_and_populate_error import SymbolAdditionError
from src.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()

def add_column_and_populate_it_by_value(
    data_frame: pl.DataFrame, column_name: str, column_value: str) -> pl.DataFrame:
    """
    Adds a new column to a given Polars DataFrame and populates it with a specified value.
    """
    try:
        # Add a new column with the specified value for all rows
        data_frame = data_frame.with_columns(pl.lit(column_value).alias(column_name))
        return data_frame
    except Exception as error:
        logger.error("Error during symbol addition: %s", error)
        raise SymbolAdditionError from error
