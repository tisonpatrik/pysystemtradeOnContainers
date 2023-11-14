"""
Module for aggregating time-based price data to daily averages.
"""
import logging

import pandas as pd

from src.common_utils.errors.aggregation_errors import DataAggregationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def aggregate_to_day_based_prices(
    data_frame: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    """
    Aggregates the time-based price data to daily averages.
    """
    try:
        # Set DATETIME as index
        series = data_frame.set_index(date_time_column)
        # Resample to daily frequency using the mean of the prices for each day
        result = series.resample("1B").last().reset_index()
        return result
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    """
    Concatenates a list of data frames into a single data frame.
    """
    try:
        return pd.concat(processed_data_frames, ignore_index=True)
    except Exception as error:
        logger.error("Failed to concatenate data frames: %s", error)
        raise
