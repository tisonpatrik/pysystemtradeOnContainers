from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp
from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe, convert_list_dicts_to_dataframe
import pandas as pd
from typing import cast

class DailyReturnsVol(DataFrameModel):
    date_time: Timestamp = Field(coerce=True) # type: ignore[assignment]
    vol: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls, items: dict) -> pd.Series:
        data = convert_dict_to_dataframe(items,
            str(DailyReturnsVol.date_time),
            str(DailyReturnsVol.vol))
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame,
            str(DailyReturnsVol.date_time),
            str(DailyReturnsVol.vol))
        return series

    @classmethod
    def from_api_to_series(cls, items: dict) -> pd.Series:
        data = convert_dict_to_dataframe(items,
            str(DailyReturnsVol.date_time),
            str(DailyReturnsVol.vol))
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame,
            str(DailyReturnsVol.date_time),
            str(DailyReturnsVol.vol))
        return series
