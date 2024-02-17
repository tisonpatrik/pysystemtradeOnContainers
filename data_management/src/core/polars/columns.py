"""
Module for handling methods for renaming columns.
"""

from typing import List

import pandas as pd
import polars as pl
from src.core.errors.rename_colums_errors import ColumnRenameError
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def rename_columns(
    data_frame: pd.DataFrame, new_column_names: List[str]
) -> pd.DataFrame:
    """
    Renames DataFrame columns based on the provided list of new column names.
    """
    try:
        data_frame.columns = new_column_names
        return data_frame
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error


def retype_dataframe(df: pl.DataFrame, schema):
    for field, field_type in schema.__annotations__.items():
        if field in df.columns:
            df = df.with_columns(df[field].cast(field_type))
    return df
