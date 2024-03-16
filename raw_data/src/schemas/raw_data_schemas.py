from datetime import datetime

import pandera as pa
from pandera.typing import Series


class AdjustedPrices(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    price: Series[float]


class FxPrices(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    price: Series[float]


class MultiplePrices(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    carry: Series[float] = pa.Field(nullable=True)
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float] = pa.Field(nullable=True)
    forward_contract: Series[int]


class RollCalendars(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
