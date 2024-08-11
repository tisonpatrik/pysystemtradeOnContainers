import pandas as pd

def apply_abs_min(x: pd.Series, min_value: float = 0.1) -> pd.Series:
    x[(x < min_value) & (x > 0)] = min_value
    x[(x > -min_value) & (x < 0)] = -min_value
    return x
