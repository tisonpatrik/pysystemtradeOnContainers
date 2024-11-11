import pandas as pd


def simple_ewvol_calc(daily_returns: pd.Series, days: int = 35, min_periods: int = 10) -> pd.Series:
    # Standard deviation will be nan for first 10 non nan values
    return daily_returns.ewm(adjust=True, span=days, min_periods=min_periods).std()
