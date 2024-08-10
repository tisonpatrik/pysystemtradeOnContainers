from typing import cast

import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp

from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe, convert_list_dicts_to_dataframe


class DailyPrices(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    price: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls, items: dict) -> pd.Series:
        data = convert_dict_to_dataframe(items, str(DailyPrices.date_time), str(DailyPrices.price))
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, str(DailyPrices.date_time), str(DailyPrices.price))
        return series

    @classmethod
    def from_db_to_series(cls, items: list[dict]) -> pd.Series:
        columns_names = list(cls.__annotations__.keys())
        data = convert_list_dicts_to_dataframe(items, str(DailyPrices.date_time), columns_names)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, str(DailyPrices.date_time), str(DailyPrices.price))
        return series
