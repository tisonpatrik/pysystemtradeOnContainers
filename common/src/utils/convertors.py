from typing import Optional, Type, TypeVar

import pandas as pd
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def to_pydantic(item: Optional[dict], model: Type[T]) -> Optional[T]:
    if item is None:
        return None
    else:
        return model(**item)

def convert_dataframe_to_series(data_frame: pd.DataFrame, index: str, values: str)-> pd.Series:
    series = pd.Series(data_frame[values].values,index=data_frame[index])
    return series
