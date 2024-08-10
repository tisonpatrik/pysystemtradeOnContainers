from typing import TypeVar, Generic, List, Type, cast, ClassVar
import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Timestamp
from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe, convert_list_dicts_to_dataframe

T = TypeVar('T', bound=DataFrameModel)

class BaseDataFrameModel(DataFrameModel, Generic[T]):
    date_time: ClassVar[Timestamp] = Field(coerce=True)  # type: ignore[assignment]

    @classmethod
    def from_cache_to_series(cls: Type[T], items: dict, value_field: str) -> pd.Series:
        data = convert_dict_to_dataframe(items, 'date_time', value_field)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, 'date_time', value_field)
        return series

    @classmethod
    def from_db_to_series(cls: Type[T], items: List[dict], value_field: str) -> pd.Series:
        columns_names = list(cls.__annotations__.keys())
        data = convert_list_dicts_to_dataframe(items, 'date_time', columns_names)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, 'date_time', value_field)
        return series

    @classmethod
    def from_db_to_dataframe(cls: Type[T], items: List[dict]) -> pd.DataFrame:
        columns_names = list(cls.__annotations__.keys())
        data = convert_list_dicts_to_dataframe(items, 'date_time', columns_names)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        return data_frame

    @classmethod
    def from_api_to_series(cls: Type[T], items: dict, value_field: str) -> pd.Series:
        data = convert_dict_to_dataframe(items, 'date_time', value_field)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, 'date_time', value_field)
        return series
