import pandera as pa
from pandera import Field
from pandera.typing import Series


class AdjustedPricesSchema(pa.DataFrameModel):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class FxPricesSchema(pa.DataFrameModel):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class MultiplePricesSchema(pa.DataFrameModel):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    carry: Series[float]
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float]
    forward_contract: Series[int]


class RollCalendarsSchema(pa.DataFrameModel):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
