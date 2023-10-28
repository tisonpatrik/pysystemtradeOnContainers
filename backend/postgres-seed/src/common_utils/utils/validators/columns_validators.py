import logging
from typing import Dict

import pandas as pd

from src.common_utils.errors.rename_colums_errors import (
    ColumnNoneValueError,
    MissingColumnsError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_missing_columns(data_frame: pd.DataFrame, new_column_names: Dict[str, str]):
    """
    Checks for missing columns in the data frame.
    """
    for column in new_column_names.keys():
        check_single_missing_column(data_frame, column)


def check_single_missing_column(data_frame: pd.DataFrame, column: str):
    """
    Checks for a single missing column in the data frame.
    """
    if column not in data_frame.columns:
        logger.error("Column '%s' does not exist in the DataFrame", column)
        raise MissingColumnsError(f"Column {column} does not exist")


def check_for_none_values(new_column_names: Dict[str, str]):
    """
    Checks for None values in the new column names.
    """
    for old_name, new_name in new_column_names.items():
        if new_name is None:
            logger.error("New column name cannot be None for %s", old_name)
            raise ColumnNoneValueError(f"New column name cannot be None for {old_name}")
