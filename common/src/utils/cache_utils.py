import numpy as np
import pandas as pd


def get_series_key(name: str, symbol: str) -> str:
    parts = ["series", name, "of", symbol]
    return ":".join(parts)


def convert_datetime_to_unix(series: pd.Series) -> pd.Series:
    try:
        # Create a copy of the series
        series_copy = series.copy()
        # Convert DatetimeIndex to Unix time using astype and integer division
        series_copy.index = series_copy.index.view(np.int64) // 10**9
        return series_copy
    except Exception as e:
        raise ValueError(f"Error converting DatetimeIndex to Unix time: {e!s}") from e
