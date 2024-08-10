from typing import cast

import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp

from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe


class NormalizedPricesForAssetClass(DataFrameModel):
    date_time: Timestamp = Field(coerce=True) # type: ignore[assignment]
    vol: Float = Field(coerce=True, nullable=True)


    @classmethod
    def from_api_to_series(cls, items: dict) -> pd.Series:
        data = convert_dict_to_dataframe(items,
            str(NormalizedPricesForAssetClass.date_time),
            str(NormalizedPricesForAssetClass.vol))
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame,
            str(NormalizedPricesForAssetClass.date_time),
            str(NormalizedPricesForAssetClass.vol))
        return series
