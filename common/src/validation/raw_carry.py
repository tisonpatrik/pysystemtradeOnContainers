from typing import cast

import pandas as pd
from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Int, Timestamp

from common.src.utils.convertors import convert_list_dicts_to_dataframe


class RawCarry(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    price: Float = Field(coerce=True, nullable=True)
    carry: Float = Field(coerce=True, nullable=True)
    price_contract: Int = Field(coerce=True, nullable=True)
    carry_contract: Int = Field(coerce=True, nullable=True)

    @classmethod
    def from_db_to_dataframe(cls, items: list[dict]) -> pd.DataFrame:
        columns_names = list(cls.__annotations__.keys())
        data = convert_list_dicts_to_dataframe(items, str(RawCarry.date_time), columns_names)

        validated_data = cls.validate(data)
        data_frame = cast(pd.DataFrame, validated_data)
        return data_frame
