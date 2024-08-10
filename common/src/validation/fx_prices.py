from typing import cast
import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp

# Assuming these functions exist in your utils or converters module
from common.src.utils.convertors import convert_list_dicts_to_dataframe, convert_dataframe_to_series

class FxPrices(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    price: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_db_to_series(cls, items: list[dict]) -> pd.Series:
        columns_names = list(cls.__annotations__.keys())

        data = convert_list_dicts_to_dataframe(items, str(FxPrices.date_time), columns_names)
        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        series = convert_dataframe_to_series(data_frame, str(FxPrices.date_time), str(FxPrices.price))

        return series
