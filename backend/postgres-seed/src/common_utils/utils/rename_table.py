"""
Module for handling methods for renaming columns.
"""

import logging
import pandas as pd
from typing import Dict
from src.data_processor.errors.table_helper_errors import ColumnRenameError
from src.common_utils.utils.data_frame_validators import (
    check_missing_columns,
    check_for_none_values,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rename_columns(
    data_frame: pd.DataFrame, new_column_names: Dict[str, str]
) -> pd.DataFrame:
    """
    Renames DataFrame columns based on the provided dictionary.
    """
    check_missing_columns(data_frame, new_column_names)
    check_for_none_values(new_column_names)
    try:
        return data_frame.rename(columns=new_column_names)
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error
