"""
Module for handling methods for renaming columns.
"""

from typing import List

import pandas as pd

from common.logging.logging import AppLogger

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
    except Exception as exc:
        error_message = f"rror during column renaming {str(exc)}"
        logger.error(error_message)
        raise ValueError(error_message)
