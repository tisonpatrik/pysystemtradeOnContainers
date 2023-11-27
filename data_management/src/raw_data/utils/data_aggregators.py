"""
Module for aggregating time-based price data to daily averages.
"""
import pandas as pd
from src.core.errors.aggregation_errors import (
    DataAggregationError,
    DataFrameConcatenationError,
)
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def aggregate_to_day_based_prices(
    data_frame: pd.DataFrame, date_time_column: str, price_column: str
) -> pd.DataFrame:
    """
    Aggregates the time-based price data to daily averages using Pandas.
    """
    try:
        # Ensure the date_time_column is in datetime format
        data_frame[date_time_column] = pd.to_datetime(data_frame[date_time_column])

        # Set the datetime column as the index
        data_frame = data_frame.set_index(date_time_column)

        # Resample and aggregate to get the last price of each day
        result = data_frame.resample("1D")[price_column].last()
        return result.reset_index()
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    """
    Concatenates a list of Pandas data frames into a single data frame.
    """
    try:
        return pd.concat(processed_data_frames)
    except Exception as error:
        logger.error("Failed to concatenate data frames: %s", error)
        raise DataFrameConcatenationError from error
