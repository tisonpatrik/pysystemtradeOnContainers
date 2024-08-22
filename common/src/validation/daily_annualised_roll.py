from pandera import Field
from pandera.dtypes import Float, Timestamp
import pandas as pd
from typing import TypeVar, Type
from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar('T', bound='DailyAnnualisedRoll')

class DailyAnnualisedRoll(BaseDataFrameModel[T]):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    vdaily_rollol: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls: Type[T], items: dict, values_column: str = 'vol') -> pd.Series:
        return super().from_cache_to_series(items, values_column)

    @classmethod
    def from_api_to_series(cls: Type[T], items: dict, values_column: str = 'vol') -> pd.Series:
        return super().from_api_to_series(items, values_column)
