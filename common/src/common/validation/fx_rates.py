from typing import TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float

from common.validation.base_data_model import BaseDataFrameModel

T = TypeVar("T", bound="FxRates")


class FxRates(BaseDataFrameModel[T]):
    values: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls: type[T], items: dict, values_column: str = "values") -> pd.Series:
        return super().from_cache_to_series(items, values_column)

    @classmethod
    def from_db_to_series(cls: type[T], items: list[dict], value_field: str = "values") -> pd.Series:
        return super().from_db_to_series(items, value_field)
