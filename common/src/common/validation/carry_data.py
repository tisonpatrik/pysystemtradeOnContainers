from typing import TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float, Int

from common.validation.base_data_model import BaseDataFrameModel

T = TypeVar("T", bound="CarryData")


class CarryData(BaseDataFrameModel[T]):
    price: Float = Field(coerce=True, nullable=True)
    carry: Float = Field(coerce=True, nullable=True)
    price_contract: Int = Field(coerce=True, nullable=True)
    carry_contract: Int = Field(coerce=True, nullable=True)

    @classmethod
    def from_db_to_dataframe(cls: type[T], items: list[dict]) -> pd.DataFrame:
        return super().from_db_to_dataframe(items)
