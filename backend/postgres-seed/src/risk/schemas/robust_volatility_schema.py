"""
This module defines the RobustVolatilitySchema class, 
which models the structure of the 'robust_volatility' table in the database.
"""

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class RobustVolatilitySchema:
    """
    Defines the schema for the Robust Volatility table in the database.
    """

    source_table = "adjusted_prices"
    datetime_table = "unix_date_time"
    symbol_table = "symbol"
