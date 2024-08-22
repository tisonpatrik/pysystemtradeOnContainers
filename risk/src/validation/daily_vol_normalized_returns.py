from typing import Type, TypeVar

import pandas as pd
from pandera import Field
from pandera.dtypes import Float, Timestamp

from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar('T', bound='DailyvolNormalizedReturns')


class DailyvolNormalizedReturns(BaseDataFrameModel[T]):
    time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    returns: Float = Field(coerce=True, nullable=True)

    @classmethod
    def from_api_to_series(cls: Type[T], items: dict, values_column: str = 'vol') -> pd.Series:
        return super().from_api_to_series(items, values_column)
