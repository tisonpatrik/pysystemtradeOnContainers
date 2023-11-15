"""
This module contains utility functions for validating columns in a pandas DataFrame.
"""
import logging
from typing import Dict

import pandas as pd

from src.core.errors.rename_colums_errors import (
    ColumnNoneValueError,
    MissingColumnsError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_single_missing_column(data_frame: pd.DataFrame, column: str):
    """
    Checks for a single missing column in the data frame.
    """
    if column not in data_frame.columns:
        logger.error("Column '%s' does not exist in the DataFrame", column)
        raise MissingColumnsError(f"Column {column} does not exist")