from typing import Optional, Type, TypeVar

import pandas as pd
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def to_pydantic(item: Optional[dict], model: Type[T]) -> Optional[T]:
    if item is None:
        return None
    else:
        return model(**item)

def convert_list_dicts_to_dataframe(items: list[dict], index_column: str, values_columns: list) -> pd.DataFrame:
    try:
        data = pd.DataFrame(items)
        data.columns = values_columns

        data[index_column] = pd.to_numeric(data[index_column])
        data[index_column] = pd.to_datetime(data[index_column], errors='coerce').dt.strftime("%Y-%m-%d")
        return data
    except Exception as e:
        raise ValueError(f"Error converting list to DataFrame: {str(e)}")

def convert_dict_to_dataframe(raw_data: dict, index_column: str, values_column: str) -> pd.DataFrame:
    try:
        data = pd.DataFrame(list(raw_data.items()), columns=[index_column, values_column])
        data[index_column] = pd.to_numeric(data[index_column])
        data[index_column] = pd.to_datetime(data[index_column], unit='s')
        return data
    except Exception as e:
        raise ValueError(f"Error converting cache data to Series: {str(e)}")

def convert_dataframe_to_series(data_frame: pd.DataFrame, index: str, values: str)-> pd.Series:
    series = pd.Series(data_frame[values].values,index=data_frame[index])
    return series
