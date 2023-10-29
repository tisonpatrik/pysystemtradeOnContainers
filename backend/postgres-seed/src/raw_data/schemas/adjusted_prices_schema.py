"""
This module defines the schema for adjusted prices as well as utility methods related to it.
"""

from dataclasses import dataclass, field

import pandas as pd


def empty_series() -> pd.Series:
    """
    Returns an empty Pandas Series.
    """
    return pd.Series()


@dataclass(frozen=True)
class AdjustedPricesSchema:
    """
    Encapsulates a Pandas Series specifically for adjusted prices.
    """

    table_name: str = field(default="adjusted_prices")
    index_column: str = field(default="unix_date_time")
    symbol_column: str = field(default="symbol")
