import pandas as pd
from dataclasses import dataclass, field


def empty_series() -> pd.Series:
    return pd.Series()


@dataclass(frozen=True)
class AdjustedPricesSchema:
    """
    Encapsulates a Pandas Series specifically for adjusted prices.
    """

    table_name: str = field(default="adjusted_prices")
    index_column: str = field(default="unix_date_time")
    symbol_column: str = field(default="symbol")
