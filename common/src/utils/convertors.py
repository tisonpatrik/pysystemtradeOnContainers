from typing import TypeVar

import pandas as pd
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_pydantic(item: dict | None, model: type[T]) -> T | None:
    if item is None:
        return None
    return model(**item)


def convert_dataframe_to_series(data_frame: pd.DataFrame, index: str, values: str) -> pd.Series:
    return pd.Series(data_frame[values].values, index=data_frame[index])
