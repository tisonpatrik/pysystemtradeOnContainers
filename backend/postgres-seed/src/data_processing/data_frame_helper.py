"""
Data Frame Helper module.

This module provides utility functions to preprocess and transform pandas DataFrames. 
It provides functions to rename columns, handle empty values, add symbols, convert 
datetime columns to UNIX timestamp, and aggregate raw prices to daily averages.
"""

import logging
import os

import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rename_columns_if_needed(
    data_frame: pd.DataFrame, column_mapping: dict = None
) -> pd.DataFrame:
    """Rename DataFrame columns based on the provided column mapping."""
    if column_mapping:
        data_frame.rename(columns=column_mapping, inplace=True)
        logger.info("Columns renamed according to provided mapping.")
    return data_frame


def fill_empty_values(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Handle empty values within the DataFrame."""
    data_frame.fillna("", inplace=True)
    data_frame = data_frame.applymap(lambda x: "" if x == "" else x)
    return data_frame


def add_symbol_by_file_name(data_frame: pd.DataFrame, file_path: str) -> pd.DataFrame:
    """
    Adds a 'symbol' column to the DataFrame by extracting the file name from the provided file path.
    """
    try:
        symbol = os.path.splitext(os.path.basename(file_path))[0]
        data_frame["symbol"] = symbol
        logger.info("Successfully added symbol '%s' from file path '%s'.", symbol, file_path)
    except Exception as error:
        logger.error("Error adding symbol from file path '%s': %s", file_path, error)
        raise
    return data_frame


def convert_datetime_to_unixtime(data_frame: pd.DataFrame, date_time_name: str) -> pd.DataFrame:
    """
    Convert a datetime column in the DataFrame to UNIX timestamp.
    """
    try:
        data_frame[date_time_name] = pd.to_datetime(data_frame[date_time_name])
        data_frame[date_time_name] = data_frame[date_time_name].apply(lambda x: int(x.timestamp()))
        logger.info("Successfully converted column '%s' to UNIX timestamp.", date_time_name)
        return data_frame
    except Exception as error:
        logger.error("Error converting column '%s' to UNIX timestamp: %s", date_time_name, error)
        raise


def aggregate_to_day_based_prices(
    data_frame: pd.DataFrame, index_column: str, price_column: str
) -> pd.DataFrame:
    """
    Convert a dictionary of raw prices to a DataFrame, set a datetime index,
    and aggregate to provide average daily prices.
    """
    try:
        data_frame[index_column] = pd.to_datetime(data_frame[index_column])
        data_frame.set_index(index_column, inplace=True)
        data_frame[price_column] = pd.to_numeric(data_frame[price_column])
        daily_summary = data_frame.resample("D").mean()
        daily_summary.dropna(subset=[price_column], inplace=True)
        logger.info("Successfully aggregated raw prices to daily averages.")
        return daily_summary.reset_index()
    except Exception as error:
        logger.error("Error aggregating to day-based prices: %s", error)
        raise

def convert_to_dataframe(rows: list) -> pd.DataFrame:
    """Converts fetched rows into a DataFrame."""
    logger.info("Converting fetched rows to DataFrame.")
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows, columns=[desc[0] for desc in rows[0].keys()])
