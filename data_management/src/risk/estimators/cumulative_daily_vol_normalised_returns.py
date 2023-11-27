import pandas as pd
from src.risk.estimators.daily_returns import daily_returns, daily_returns_volatility


def get_cumulative_daily_vol_normalised_returns(daily_prices: pd.Series) -> pd.Series:
    """
    Returns a cumulative normalised return. This is like a price, but with equal expected vol
    Used for a few different trading rules
    """

    norm_returns = get_daily_vol_normalised_returns(daily_prices)

    cum_norm_returns = norm_returns.cumsum()

    return cum_norm_returns


def get_daily_vol_normalised_returns(daily_prices: pd.Series) -> pd.Series:
    """
    Get returns normalised by recent vol
    Useful statistic, also used for some trading rules
    """
    returnvol = daily_returns_volatility(daily_prices).shift(1)
    dailyreturns = daily_returns(daily_prices)
    norm_return = dailyreturns / returnvol

    return norm_return
