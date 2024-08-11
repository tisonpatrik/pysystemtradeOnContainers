import pandas as pd

def uniquets_series(x: pd.Series) -> pd.Series:
    """
    Makes x unique
    """
    x = x.groupby(level=0).last()
    return x
