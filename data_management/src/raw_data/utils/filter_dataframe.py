from typing import List

import pandas as pd


def filter_df_by_symbols(df: pd.DataFrame, symbols: List[str]) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows where the 'symbol' column
    matches one of the strings in the provided list.
    """
    # Check if the 'symbol' column exists in the DataFrame
    if "symbol" not in df.columns:
        raise ValueError("The DataFrame does not have a 'symbol' column.")

    # Filter the DataFrame using boolean indexing
    filtered_df = df[df["symbol"].isin(symbols)]
    return filtered_df
