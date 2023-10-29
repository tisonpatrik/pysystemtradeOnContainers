import logging
import pandas as pd

from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
)
from src.common_utils.utils.validators.columns_validators import (
    check_single_missing_column,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_grouped_df(df: pd.DataFrame, symbol_column: str) -> dict[str, pd.DataFrame]:
    """Group DataFrame by symbol column and return as a dictionary."""
    grouped_dict = {}
    try:
        grouped = df.groupby(symbol_column)
        for name, group in grouped:
            grouped_dict[str(name)] = group
        return grouped_dict
    except Exception as e:
        logger.error(f"Failed to group DataFrame: {e}")
        raise


def convert_group_to_series(
    group: dict[str, pd.DataFrame], symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    """Convert a group to a pandas Series mapped by symbol."""
    symbol = list(group.keys())[0]
    data_frame = list(group.values())[0]
    group_dropped = data_frame.drop(columns=[symbol_column])
    series = group_dropped.set_index(index_column).squeeze()
    return {symbol: series}


def convert_dataframe_to_list_of_series(
    df: pd.DataFrame, symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    """
    Converts the DataFrame to a list of SeriesSchema objects.
    """
    logger.info("Processing dataframes to series")

    check_single_missing_column(df, symbol_column)
    check_single_missing_column(df, index_column)
    time_converted = convert_column_to_datetime(df, index_column, "s")
    try:
        dicted_data_frames = get_grouped_df(time_converted, symbol_column)
        series_dict = {}

        for symbol, data_frame in dicted_data_frames.items():
            series = convert_group_to_series(
                {symbol: data_frame}, symbol_column, index_column
            )
            series_dict[symbol] = series[symbol]
    except Exception as e:
        logger.error(
            f"An error occurred while converting DataFrame to SeriesSchemas: {e}"
        )
        raise

    return series_dict
