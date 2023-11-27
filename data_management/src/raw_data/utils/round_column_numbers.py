"""
This module provides functionalities for rounding values in specific columns of a Pandas DataFrame.

It imports pandas for data manipulation and uses a custom exception for errors related to column rounding.
The module also imports a utility function for checking missing columns.
"""

import pandas as pd
from src.core.utils.logging import AppLogger
from src.raw_data.errors.rounding_error import ColumnRoundingError

logger = AppLogger.get_instance().get_logger()


def round_values_in_column(
    data_frame: pd.DataFrame, column_to_round: str
) -> pd.DataFrame:
    """
    Rounds the values in a specific column of a Pandas DataFrame.
    """
    try:
        if column_to_round in data_frame.columns:
            data_frame[column_to_round] = data_frame[column_to_round].round(3)
        else:
            raise KeyError(f"Column '{column_to_round}' not found in DataFrame.")
    except KeyError as ke:
        logger.error("Column not found error: %s", ke)
        raise ColumnRoundingError(f"Error rounding column '{column_to_round}'") from ke
    except Exception as exc:
        logger.error("An unexpected error occurred: %s", exc)
        raise ColumnRoundingError(f"Error rounding column '{column_to_round}'") from exc

    return data_frame
