from pandera import Field
from pandera.dtypes import Float, Timestamp
import pandas as pd
from typing import TypeVar, Type, List
from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar('T', bound='FxPrices')

class FxPrices(BaseDataFrameModel[T]):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    price: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_db_to_series(cls: Type[T], items: List[dict], value_field: str = 'price') -> pd.Series:
        return super().from_db_to_series(items, value_field)
