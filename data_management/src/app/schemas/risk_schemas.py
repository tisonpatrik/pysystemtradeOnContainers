import pandera as pa
from pandera import Field
from pandera.typing import Series


class DailyReturnsVolatilitySchema(pa.DataFrameModel):
    unix_date_time: Series[int]
    symbol: Series[str] = Field(nullable=False)
    daily_returns_volatility: Series[float]


class InstrumentVolatilitySchema(pa.DataFrameModel):
    unix_date_time: Series[int]
    symbol: Series[str] = Field(nullable=False)
    instrument_volatility: Series[float]


class DailyVolNormalizedReturnsSchema(pa.DataFrameModel):
    unix_date_time: Series[int]
    symbol: Series[str] = Field(nullable=False)
    normalized_volatility: Series[float]


class DailyVolNormalisedPriceForAssetClassSchema(pa.DataFrameModel):
    unix_date_time: Series[int]
    asset_class: Series[str] = Field(nullable=False)
    normalized_volatility: Series[float]
