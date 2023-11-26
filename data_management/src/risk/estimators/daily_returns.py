import pandas as pd
import polars as pl
from src.risk.estimators.volatility import mixed_vol_calc


def daily_returns_volatility(daily_prices: pd.Series) -> pl.DataFrame:
    """
    Calculates the daily returns volatility.
    """
    # Calculate daily returns
    price_returns = daily_returns(daily_prices)
    # Assuming mixed_vol_calc is adapted for Polars and returns a DataFrame
    # vol_multiplier can be adjusted as per your requirement
    vol_multiplier = 1
    raw_vol = mixed_vol_calc(price_returns)

    # Apply the multiplier to the volatility
    # Assuming 'volatility' is the column name in the raw_vol DataFrame
    vol = vol_multiplier * raw_vol

    vol = vol.to_frame()
    return pl.from_pandas(vol)


def daily_returns(daily_prices: pd.Series) -> pd.Series:
    """
    Gets daily returns (not % returns)
    """
    dailyreturns = daily_prices.diff()
    return dailyreturns
