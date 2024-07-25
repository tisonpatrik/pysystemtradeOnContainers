import pandas as pd


def ewmac(price: pd.Series, vol: pd.Series, Lfast: int, Lslow: int) -> pd.Series:
    fast_ewma = price.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = price.ewm(span=Lslow, min_periods=1).mean()
    raw_ewmac = fast_ewma - slow_ewma

    return raw_ewmac / vol.ffill()
