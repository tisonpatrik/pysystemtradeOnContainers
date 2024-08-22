from typing import ClassVar, Generic, List, Type, TypeVar, cast

import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Timestamp
from pandera.errors import SchemaError

from common.src.utils.convertors import convert_dataframe_to_series

T = TypeVar('T', bound=DataFrameModel)
index_column = 'time'

class BaseDataFrameModel(DataFrameModel, Generic[T]):
    time: ClassVar[Timestamp] = Field(coerce=True)  # type: ignore[assignment]

    @classmethod
    def from_cache_to_series(cls: Type[T], items: dict, values_column: str) -> pd.Series:
        try:
            data = pd.DataFrame(list(items.items()), columns=[index_column, values_column])
            data[index_column] = pd.to_numeric(data[index_column])
            data[index_column] = pd.to_datetime(data[index_column], unit='s')
            validated_data = cls.validate(data)
            data_frame = cast(pd.DataFrame, validated_data)
            series = convert_dataframe_to_series(data_frame, index_column, values_column)
            return series
        except SchemaError as e:
            raise ValueError(f"Data validation failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred in from_cache_to_series: {e}") from e

    @classmethod
    def from_db_to_series(cls: Type[T], items: List[dict], value_field: str) -> pd.Series:
        try:
            columns_names = list(cls.__annotations__.keys())
            data = pd.DataFrame(items)
            data.columns = columns_names

            data[index_column] = pd.to_numeric(data[index_column])
            data[index_column] = pd.to_datetime(data[index_column], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")
            validated_data = cls.validate(data)
            data_frame = cast(pd.DataFrame, validated_data)
            series = convert_dataframe_to_series(data_frame,index_column , value_field)
            return series
        except SchemaError as e:
            raise ValueError(f"Data validation failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred in from_db_to_series: {e}") from e

    @classmethod
    def from_db_to_dataframe(cls: Type[T], items: List[dict]) -> pd.DataFrame:
        try:
            columns_names = list(cls.__annotations__.keys())
            data = pd.DataFrame(items)
            data.columns = columns_names

            data[index_column] = pd.to_numeric(data[index_column])
            data[index_column] = pd.to_datetime(data[index_column], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")
            validated_data = cls.validate(data)
            data_frame = cast(pd.DataFrame, validated_data)
            return data_frame
        except SchemaError as e:
            raise ValueError(f"Data validation failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred in from_db_to_dataframe: {e}") from e

    @classmethod
    def from_api_to_series(cls: Type[T], items: dict, values_column: str) -> pd.Series:
        try:
            data = pd.DataFrame(list(items.items()), columns=[index_column, values_column])
            data[index_column] = pd.to_datetime(data[index_column], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")
            validated_data = cls.validate(data)
            data_frame = cast(pd.DataFrame, validated_data)
            series = convert_dataframe_to_series(data_frame, index_column, values_column)
            return series
        except SchemaError as e:
            raise ValueError(f"Data validation failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred in from_api_to_series: {e}") from e
