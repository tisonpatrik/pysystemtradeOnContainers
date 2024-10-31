from typing import TypeVar

import pandas as pd
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_pydantic(item: dict | None, model: type[T]) -> T | None:
    if item is None:
        return None
    return model(**item)


def convert_dataframe_to_series(data_frame: pd.DataFrame, index: str, values: str) -> pd.Series:
    sorted_data_frame = data_frame.sort_values(by=index)
    return pd.Series(sorted_data_frame[values].values, index=sorted_data_frame[index])
