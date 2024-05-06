import pandas as pd


def resample_prices_to_business_day_index(x: pd.Series) -> pd.Series:
    return x.resample("1B").last()
