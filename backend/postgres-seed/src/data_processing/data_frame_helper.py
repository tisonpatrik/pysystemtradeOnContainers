"""
Data Frame Helper module.

This module provides utility functions to preprocess and transform pandas DataFrames. 
It provides functions to rename columns, handle empty values, add symbols, convert 
datetime columns to UNIX timestamp, and aggregate raw prices to daily averages.
"""

import logging
import pandas as pd

from datetime import datetime
from src.data_processing.errors import (
    ColumnRenameError,
    EmptyValueFillError,
    DataAggregationError,
    SymbolAdditionError,
    DateTimeConversionError,)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rename_columns(data_frame, new_column_names):
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

def convert_datetime_to_unixtime(data_frame):
    """
    Converts the date_column to UNIX time.
    """
    try:
        data_frame['unix_date_time'] = pd.to_datetime(data_frame['unix_date_time']).astype(int) // 10**9
        data_frame = data_frame.dropna()
        return data_frame
    except Exception as error:
        logger.error("Error during date-time conversion: %s", error)
        raise DateTimeConversionError from error

def aggregate_to_day_based_prices(data_frame):
    try:
        data_frame['unix_date_time'] = pd.to_datetime(data_frame['unix_date_time'])
        # Ensure the aggregation_column is of a numeric type
        data_frame['price'] = pd.to_numeric(data_frame['price'], errors='coerce')

        # Set DATETIME as index
        data_frame.set_index('unix_date_time', inplace=True)

        # Resample to daily frequency using the mean of the prices for each day
        result = data_frame.resample('D').mean().dropna().reset_index()

        return result
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error