import pandera as pa
from pandera.typing import Series

from common.src.validation.base_schema import BaseSchema


class FxPricesSchema(BaseSchema):
    symbol: Series[str]
    price: Series[float]


class MultiplePricesSchema(BaseSchema):
    symbol: Series[str]
    carry: Series[float] = pa.Field(nullable=True)
    carry_contract: Series[int]
    price: Series[float]
    price_contract: Series[int]
    forward: Series[float] = pa.Field(nullable=True)
    forward_contract: Series[int]


class RollCalendarsSchema(BaseSchema):
    symbol: Series[str]
    current_contract: Series[int]
    next_contract: Series[int]
    carry_contract: Series[int]
