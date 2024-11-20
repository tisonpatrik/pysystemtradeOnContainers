from typing import TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float

from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar("T", bound="NegSkew")


class NegSkew(BaseDataFrameModel[T]):
    negskew: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls: type[T], items: dict, values_column: str = "negskew") -> pd.Series:
        return super().from_cache_to_series(items, values_column)
