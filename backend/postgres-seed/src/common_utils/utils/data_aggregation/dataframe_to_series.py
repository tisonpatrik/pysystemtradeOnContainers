import logging
import pandas as pd

from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_column_to_datetime,
)
from src.common_utils.utils.validators.columns_validators import (
    check_single_missing_column,
)
from src.common_utils.errors.dataframe_to_series_errors import (
    ColumnNotFoundError,
    GroupByError,
    DataFrameConversionError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_grouped_df(df: pd.DataFrame, symbol_column: str) -> dict[str, pd.DataFrame]:
    """Group DataFrame by symbol column and return as a dictionary."""
    try:
        return {str(name): group for name, group in df.groupby(symbol_column)}
    except Exception as e:
        logger.error(f"An unexpected error occurred while grouping DataFrame: {e}")
        raise GroupByError(e)


def convert_group_to_series(
    group: dict[str, pd.DataFrame], symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    symbol, data_frame = next(iter(group.items()))
    data_frame.drop(columns=[symbol_column], inplace=True)
    series = data_frame.set_index(index_column).squeeze()
    return {symbol: series}


def convert_dataframe_to_dict_of_series(
    df: pd.DataFrame, symbol_column: str, index_column: str
) -> dict[str, pd.Series]:
    """
    Converts the DataFrame to a dictionary of pandas Series.
    """
    logger.info("Processing dataframes to series")
    check_single_missing_column(df, symbol_column)
    check_single_missing_column(df, index_column)

    time_converted = convert_column_to_datetime(df, index_column, "s")
    series_dict = {}

    try:
        grouped_data_frames = get_grouped_df(time_converted, symbol_column)

        for symbol, data_frame in grouped_data_frames.items():
            series = convert_group_to_series(
                {symbol: data_frame}, symbol_column, index_column
            )[symbol]
            series_dict[symbol] = series

    except Exception as e:
        logger.error(f"An error occurred while converting DataFrame to series: {e}")
        raise DataFrameConversionError(e)

    return series_dict
