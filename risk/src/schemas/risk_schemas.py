import pandera as pa
from pandera.typing import Series

from common.src.validation.base_schema import BaseSchema


class DailyReturnsVolatilitySchema(BaseSchema):
    symbol: Series[str] = pa.Field(nullable=False)
    daily_returns_volatility: Series[float]

class DailyReturnsVol(BaseSchema):
    daily_returns_volatility: Series[float]

class InstrumentVolatilitySchema(BaseSchema):
    symbol: Series[str] = pa.Field(nullable=False)
    instrument_volatility: Series[float]

class DailyVolNormalizedReturnsSchema(BaseSchema):
    symbol: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]

class DailyVolNormalisedPriceForAssetClassSchema(BaseSchema):
    asset_class: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]
