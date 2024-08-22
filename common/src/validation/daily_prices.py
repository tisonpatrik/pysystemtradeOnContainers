from pandera import Field
from pandera.dtypes import Float, Timestamp
import pandas as pd
from typing import TypeVar, Type, List
from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar('T', bound='DailyPrices')

class DailyPrices(BaseDataFrameModel[T]):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    vol: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_cache_to_series(cls: Type[T], items: dict, values_column: str = 'vol') -> pd.Series:
        return super().from_cache_to_series(items, values_column)

    @classmethod
    def from_db_to_series(cls: Type[T], items: List[dict], value_field: str = 'vol') -> pd.Series:
        return super().from_db_to_series(items, value_field)
