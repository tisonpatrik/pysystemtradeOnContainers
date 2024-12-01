from typing import TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float

from common.validation.base_data_model import BaseDataFrameModel

T = TypeVar("T", bound="AbsoluteSkewDeviation")


class AbsoluteSkewDeviation(BaseDataFrameModel[T]):
    skw: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_api_to_series(cls: type[T], items: dict, values_column: str = "skw") -> pd.Series:
        return super().from_api_to_series(items, values_column)

    @classmethod
    def from_cache_to_series(cls: type[T], items: dict, values_column: str = "skw") -> pd.Series:
        return super().from_cache_to_series(items, values_column)