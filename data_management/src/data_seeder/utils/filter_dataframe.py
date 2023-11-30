from typing import List

import polars as pl


def filter_df_by_symbols(df: pl.DataFrame, symbols: List[str]) -> pl.DataFrame:
    """
    Filters the DataFrame to include only rows where the 'symbol' column
    matches one of the strings in the provided list.
    """
    # Check if the 'symbol' column exists in the DataFrame
    if "symbol" not in df.columns:
        raise ValueError("The DataFrame does not have a 'symbol' column.")

    # Filter the DataFrame
    filtered_df = df.filter(df["symbol"].is_in(symbols))
    return filtered_df