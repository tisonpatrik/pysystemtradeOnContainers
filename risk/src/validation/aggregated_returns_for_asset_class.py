from typing import cast
import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp

from common.src.utils.convertors import convert_dataframe_to_series, convert_dict_to_dataframe


class AggregatedReturnsForAssetClass(DataFrameModel):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    returns: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_api_to_series(cls, items: dict) -> pd.Series:
        data = convert_dict_to_dataframe(
            items,
            str(AggregatedReturnsForAssetClass.time),
            str(AggregatedReturnsForAssetClass.returns)
        )

        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)

        series = convert_dataframe_to_series(
            data_frame,
            str(AggregatedReturnsForAssetClass.time),
            str(AggregatedReturnsForAssetClass.returns)
        )

        return series
