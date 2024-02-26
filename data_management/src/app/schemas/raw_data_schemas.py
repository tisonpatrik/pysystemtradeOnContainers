import pandera as pa
from pandera import Field
from pandera.typing import Series


class AdjustedPricesSchema(pa.SeriesSchema):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class FxPricesSchema(pa.SeriesSchema):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    price: Series[float]


class MultiplePricesSchema(pa.SeriesSchema):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    carry: Series[float] = Field(nullable=True)
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float] = Field(nullable=True)
    forward_contract: Series[int]


class RollCalendarsSchema(pa.SeriesSchema):
    unix_date_time: Series[int] = Field(gt=0)
    symbol: Series[str] = Field(nullable=False)
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
