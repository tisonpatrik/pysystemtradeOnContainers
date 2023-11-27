"""
Module for handling methods for renaming columns.
"""

import pandas as pd
from src.core.errors.rename_colums_errors import ColumnRenameError
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def rename_columns(data_frame: pd.DataFrame, new_column_names: list):
    """
    Renames DataFrame columns based on the provided list of new column names.
    """
    try:
        if len(data_frame.columns) != len(new_column_names):
            raise ValueError(
                "The number of new column names must match the number of existing columns"
            )

        data_frame.columns = new_column_names
        return data_frame

    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error
