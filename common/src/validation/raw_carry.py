from pandera import Field
from pandera.dtypes import Float, Timestamp, Int
import pandas as pd
from typing import TypeVar, Type, List
from common.src.validation.base_data_model import BaseDataFrameModel

T = TypeVar('T', bound='RawCarry')

class RawCarry(BaseDataFrameModel[T]):
    date_time: Timestamp = Field(coerce=True)  # type: ignore[assignment]
    price: Float = Field(coerce=True, nullable=True)
    carry: Float = Field(coerce=True, nullable=True)
    price_contract: Int = Field(coerce=True, nullable=True)
    carry_contract: Int = Field(coerce=True, nullable=True)

    @classmethod
    def from_db_to_dataframe(cls: Type[T], items: List[dict]) -> pd.DataFrame:
        return super().from_db_to_dataframe(items)
