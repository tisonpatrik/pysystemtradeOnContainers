"""
Module for handling methods for renaming columns.
"""

import polars as pl
from src.core.errors.rename_colums_errors import ColumnRenameError


from src.utils.logging import AppLogger
logger = AppLogger.get_instance().get_logger()

def rename_columns(data_frame, new_column_names):
    """
    Renames DataFrame columns based on the provided list of new column names.
    """
    try:
        data_frame.columns = new_column_names
        return data_frame
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error

def remove_unnamed_columns(data_frame: pl.DataFrame):
    """
    Removes unnamed columns from a given pandas DataFrame.
    """
    removed_unnamed_columns = data_frame.loc[
        :, ~data_frame.columns.str.contains("^Unnamed")
    ]
    return removed_unnamed_columns
