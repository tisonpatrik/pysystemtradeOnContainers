"""
This module defines the RobustVolatilitySchema class, 
which models the structure of the 'robust_volatility' table in the database.
"""

from dataclasses import dataclass


@dataclass
class RobustVolatilitySchema:
    """
    Defines the schema for the Robust Volatility table in the database.
    """

    def __init__(self):
        """
        Initialize the DataFrameContainer with a DataFrame and a table name.
        """
        self.source_table = "adjusted_prices"
        self.datetime_table = "unix_date_time"
        self.symbol_table = "symbol"
