
from pandera.typing import Series

from common.src.validation.base_schema import BaseSchema


class AdjustedPricesSchema(BaseSchema):
    symbol: Series[str]
    price: Series[float]

class DailyPricesSchema(BaseSchema):
    price: Series[float]
