from bisect import bisect_left, insort_left

import numpy as np
import pandas as pd


def calculate_quantile_of_points_in_data_series(normalised_vol: pd.Series) -> pd.Series:
    """Calculate the quantile of each point in the series based on previous values."""
    sorted_values: list[int] = []
    results = []
    for current_value in normalised_vol:
        position = bisect_left(sorted_values, current_value)
        results.append(position / (len(sorted_values) + 1))
        insort_left(sorted_values, current_value)

    return pd.Series(results, index=normalised_vol.index)


def multiplier_function( normalised_vol_q: pd.Series) -> pd.Series:
    """Apply a multiplier function based on quantile values."""
    vol_attenuation = np.where(
        np.isnan(normalised_vol_q),
        1.0,
        2 - 1.5 * normalised_vol_q,
    )
    return pd.Series(vol_attenuation, index=normalised_vol_q.index)
