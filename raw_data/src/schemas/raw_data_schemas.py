import pandas as pd
import pandera as pa
from pandera import Field
from pandera.typing import Series


class AdjustedPricesSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class FxPricesSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class MultiplePricesSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = Field(nullable=False)
    carry: Series[float] = Field(nullable=True)
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float] = Field(nullable=True)
    forward_contract: Series[int]


class RollCalendarsSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = Field(nullable=False)
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
