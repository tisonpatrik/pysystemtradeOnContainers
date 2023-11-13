"""Module for converting data frames to dictionaries of pandas Series."""

import logging

import pandas as pd

from src.common_utils.errors.dataframe_to_series_errors import (
    DataFrameConversionError,
    GroupByError,
)
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
)
from src.common_utils.utils.validators.columns_validators import (
    check_single_missing_column,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_grouped_df(
    data_frame: pd.DataFrame, symbol_column: str
) -> dict[str, pd.DataFrame]:
    """Group DataFrame by symbol column and return as a dictionary."""
    try:
        return {str(name): group for name, group in data_frame.groupby(symbol_column)}
    except Exception as exc:
        logger.error("An unexpected error occurred while grouping DataFrame: %s", exc)
        raise GroupByError(exc) from exc


def convert_group_to_series(
    group: dict[str, pd.DataFrame], symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    """Convert a group of data frames to a dictionary of pandas Series."""
    symbol, data_frame = next(iter(group.items()))
    data_frame.drop(columns=[symbol_column], inplace=True)
    series = data_frame.set_index(index_column).squeeze()
    return {symbol: series}


def convert_dataframe_to_dict_of_series(
    data_frame: pd.DataFrame, symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    logger.info("Processing dataframes to series")
    check_single_missing_column(data_frame, symbol_column)
    check_single_missing_column(data_frame, index_column)

    time_converted = convert_column_to_datetime(data_frame, index_column, "s")
    series_dict = {}

    try:
        grouped_data_frames = get_grouped_df(time_converted, symbol_column)
        for symbol, frame in grouped_data_frames.items():
            series = convert_group_to_series(
                {symbol: frame}, symbol_column, index_column
            )[symbol]
            series_dict[symbol] = series
    except Exception as exc:
        logger.error("An error occurred while converting DataFrame to series: %s", exc)
        raise DataFrameConversionError(exc) from exc

    return series_dict


def convert_dataframe_to_serie(
    data_frame: pd.DataFrame, index_column: str
) -> pd.Series:
    """Converts the DataFrame to pandas Series."""
    check_single_missing_column(data_frame, index_column)

    time_converted = convert_column_to_datetime(data_frame, index_column, "s")
    time_converted_sorted = time_converted.sort_values(by=index_column)
    series = time_converted_sorted.set_index(index_column).squeeze()

    return series
