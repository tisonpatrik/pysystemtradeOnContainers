import logging

import pandas as pd
from src.common_utils.utils.columns_validators import check_single_missing_column
from src.common_utils.errors.rounding_error import ColumnRoundingError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def round_values_in_column(
    data_frame: pd.DataFrame, column_to_round: str
) -> pd.DataFrame:
    """
    Rounds the values in a specific column of a Pandas DataFrame.
    """
    try:
        check_single_missing_column(data_frame, column_to_round)
        data_frame[column_to_round] = data_frame[column_to_round].round(1)
    except Exception as error:
        logger.error("An unexpected error occurred: %s", error)
        raise ColumnRoundingError(
            f"Error rounding column '{column_to_round}'"
        ) from error

    return data_frame
