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


def list_to_series(items: list[dict], model: Type[T], index_column: str, values_column: str) -> pd.Series:
    try:
        raw_frame = pd.DataFrame(items)
        data = raw_frame.rename(columns={raw_frame.columns[0]: index_column, raw_frame.columns[1]: values_column})

        # Ensure the index_column is in the desired date format
        data[index_column] = pd.to_datetime(data[index_column]).dt.strftime("%Y-%m-%d")

        validated_data = model.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = pd.Series(data_frame[values_column].values, index=data_frame[index_column])
        return series
    except Exception as e:
        raise ValueError(f"Error converting list to Series: {str(e)}")


def series_to_dataframe(series: pd.Series, model: Type[T], index_column: str, values_column: str) -> pd.DataFrame:
    try:
        data = pd.DataFrame({index_column: series.index, values_column: series.values})
        validated_data = model.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        return data_frame
    except Exception as e:
        raise ValueError(f"Error converting Series to DataFrame: {str(e)}")


def dict_to_series(raw_data: dict, model: Type[T], index_column: str, values_column: str) -> pd.Series:
    try:
        data = pd.DataFrame(list(raw_data.items()), columns=[index_column, values_column])
        # Ensure the index_column is in the desired date format
        data[index_column] = pd.to_datetime(data[index_column]).dt.strftime("%Y-%m-%d")

        validated_data = model.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = pd.Series(data_frame[values_column].values, index=data_frame[index_column])
        return series
    except Exception as e:
        raise ValueError(f"Error converting JSON to Series: {str(e)}")
