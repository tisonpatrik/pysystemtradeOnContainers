"""
Data Frame Helper module.

This module provides utility functions to preprocess and transform pandas DataFrames. 
It provides functions to rename columns, handle empty values, add symbols, convert 
datetime columns to UNIX timestamp, and aggregate raw prices to daily averages.
"""

import logging

import pandas as pd
from src.data_processing.errors import (
    ColumnRenameError,
    EmptyValueFillError,
    DataAggregationError,
    SymbolAdditionError,
    DateTimeConversionError,
    EmptyDataFrameError
)
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rename_columns_if_needed(data_frame, new_column_names):
    """
    Renames DataFrame columns based on the provided dictionary.
    """
    try:
        return data_frame.rename(columns=new_column_names)
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error

def fill_empty_values(data_frame, fill_value):
    """
    Fills empty values in the DataFrame with the provided fill_value.
    """
    try:
        return data_frame.fillna(fill_value)
    except Exception as error:
        logger.error("Error during filling empty values: %s", error)
        raise EmptyValueFillError from error

def add_symbol_by_file_name(data_frame, symbol):
    """
    Adds a 'symbol' column to the DataFrame with the provided symbol.
    """
    try:
        data_frame['symbol'] = symbol
        return data_frame
    except Exception as error:
        logger.error("Error during symbol addition: %s", error)
        raise SymbolAdditionError from error

def convert_datetime_to_unixtime(data_frame, date_column):
    """
    Converts the date_column to UNIX time.
    """
    try:
        data_frame[date_column] = pd.to_datetime(data_frame[date_column]).astype(int) / 10**9
        return data_frame
    except Exception as error:
        logger.error("Error during date-time conversion: %s", error)
        raise DateTimeConversionError from error

def aggregate_to_day_based_prices(data_frame, aggregation_column):
    """
    Aggregates data based on the provided aggregation_column.
    """
    try:
        return data_frame.groupby(aggregation_column).mean().reset_index()
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error

def handle_empty_dataframe(data_frame):
    """
    Handles empty DataFrame, if needed.
    """
    if data_frame.empty:
        raise EmptyDataFrameError("DataFrame is empty.")
    return data_frame
