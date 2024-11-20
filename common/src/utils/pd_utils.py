import pandas as pd


def uniquets_series(x: pd.Series) -> pd.Series:
    """
    Makes x unique
    """
    return x.groupby(level=0).last()


def resample_prices_to_business_day_index(x: pd.Series) -> pd.Series:
    return x.resample("1B").last()


def rename_columns(data: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    if len(data.columns) != len(column_names):
        raise ValueError(
            f"Mismatch in lengths: DataFrame columns ({len(data.columns)}) - {list(data.columns)}, "
            f"New column names ({len(column_names)}) - {column_names}"
        )
    data.columns = pd.Index(column_names)
    return data
