import json
from typing import Optional, Type, TypeVar, cast

import pandas as pd
from pandera import DataFrameModel
from pydantic import BaseModel

S = TypeVar("S", bound=BaseModel)
T = TypeVar("T", bound=DataFrameModel)


def to_pydantic(item: Optional[dict], model: Type[S]) -> Optional[S]:
    if item is None:
        return None
    else:
        return model(**item)


def to_series(items: list[dict], model: Type[T], index_column: str, values_column: str) -> pd.Series:
    data = pd.DataFrame(items)
    validated_data = model.validate(data)
    data_frame = cast(pd.DataFrame, validated_data)
    series = pd.Series(data_frame[values_column].values, index=data_frame[index_column])
    return series


def to_dataframe(series: pd.Series, model: Type[T], index_column: str, values_column: str) -> pd.DataFrame:
    data = pd.DataFrame({index_column: series.index, values_column: series.values})
    validated_data = model.validate(data)
    data_frame = cast(pd.DataFrame, validated_data)
    return data_frame


def to_series_from_json(json_str: str, model: Type[DataFrameModel], index_column: str, values_column: str) -> pd.Series:
    try:
        items = json.loads(json_str)
        data = pd.DataFrame(items)
        validated_data = model.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = pd.Series(data_frame[values_column].values, index=data_frame[index_column])
        return series
    except Exception as e:
        raise ValueError(f"Error converting JSON to Series: {str(e)}")
