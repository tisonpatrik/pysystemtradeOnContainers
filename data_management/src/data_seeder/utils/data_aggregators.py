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
    data_frame: pl.DataFrame, date_time_column: str
) -> pl.DataFrame:
    """
    Aggregates the time-based price data to daily averages.
    """
    try:
        # Convert Polars DataFrame to Pandas DataFrame
        pd_frame = data_frame.to_pandas()
        # Ensure the date_time_column is in datetime format and set it as the index
        pd_frame.set_index(date_time_column, inplace=True)
        # Resample and get the last price of each business day
        resampled = pd_frame.resample("1B").last()
        # Reset the index to convert the datetime index back into a column
        resampled.reset_index(inplace=True)

        # Convert back to Polars DataFrame
        result = pl.from_pandas(resampled)

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
