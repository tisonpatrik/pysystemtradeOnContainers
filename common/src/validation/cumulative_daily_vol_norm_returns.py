from typing import TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float, Timestamp
from pandera.errors import SchemaError

from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar("T", bound="CumulativeDailyVolNormReturns")


class CumulativeDailyVolNormReturns(BaseDataFrameModel[T]):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    vol: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_api_to_series(cls: type[T], items: dict, values_column: str = "vol") -> pd.Series:
        return super().from_api_to_series(items, values_column)

    @classmethod
    def from_cache_to_series(cls: type[T], items: dict, values_column: str = "vol") -> pd.Series:
        try:
            return super().from_cache_to_series(items, values_column)
        except SchemaError as e:
            raise ValueError(f"Data validation failed in from_cache_to_series: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred in from_cache_to_series: {e}") from e
