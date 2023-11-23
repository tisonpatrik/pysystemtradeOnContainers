"""
Module for aggregating time-based price data to daily averages.
"""
import polars as pl
from src.core.errors.aggregation_errors import (
    DataAggregationError,
    DataFrameConcatenationError,
)
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def aggregate_to_day_based_prices(
    data_frame: pl.DataFrame, date_time_column: str, price_column: str
) -> pl.DataFrame:
    """
    Aggregates the time-based price data to daily averages.
    """
    try:
        result = (
            data_frame.sort(date_time_column)
            .group_by_dynamic(date_time_column, every="1d")
            .agg(pl.col(price_column).last().alias(price_column))
        )
        return result
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error


def concatenate_data_frames(processed_data_frames: list) -> pl.DataFrame:
    """
    Concatenates a list of Polars data frames into a single data frame.
    """
    try:
        return pl.concat(processed_data_frames, rechunk=True)
    except Exception as error:
        logger.error("Failed to concatenate data frames: %s", error)
        raise DataFrameConcatenationError from error
