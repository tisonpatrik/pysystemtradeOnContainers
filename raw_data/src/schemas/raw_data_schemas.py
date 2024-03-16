from datetime import datetime

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series

from common.src.validations.prices_schemas import DailyPrices


class AdjustedPricesSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    price: Series[float]


class FxPricesSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    price: Series[float]


class MultiplePricesSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    carry: Series[float] = pa.Field(nullable=True)
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float] = pa.Field(nullable=True)
    forward_contract: Series[int]


class RollCalendarsSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
