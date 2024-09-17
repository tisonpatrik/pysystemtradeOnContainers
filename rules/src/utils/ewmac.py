import pandas as pd


def ewmac(price: pd.Series, vol: pd.Series, Lfast: int, Lslow: int) -> pd.Series:
    fast_ewma = price.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = price.ewm(span=Lslow, min_periods=1).mean()
    raw_ewmac = fast_ewma - slow_ewma
    return raw_ewmac / vol.ffill()


def simple_ewvol_calc(daily_returns: pd.Series, days: int = 35, min_periods: int = 10) -> pd.Series:
    # Standard deviation will be nan for first 10 non nan values
    return daily_returns.ewm(adjust=True, span=days, min_periods=min_periods).std()
