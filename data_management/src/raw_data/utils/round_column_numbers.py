"""
This module provides functionalities for rounding values in specific columns of a Pandas DataFrame.

It imports pandas for data manipulation and uses a custom exception for errors related to column rounding.
The module also imports a utility function for checking missing columns.
"""

import polars as pl
from src.core.utils.logging import AppLogger
from src.raw_data.errors.rounding_error import ColumnRoundingError

logger = AppLogger.get_instance().get_logger()


def round_values_in_column(
    data_frame: pl.DataFrame, column_to_round: str
) -> pl.DataFrame:
    """
    Rounds the values in a specific column of a Pandas DataFrame.
    """
    try:
        data_frame = data_frame.with_columns(
            data_frame[column_to_round].round(3).alias(column_to_round)
        )
    except Exception as exc:
        logger.error("An unexpected error occurred: %s", exc)
        raise ColumnRoundingError(f"Error rounding column '{column_to_round}'") from exc

    return data_frame
