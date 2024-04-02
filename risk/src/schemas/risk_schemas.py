from datetime import datetime

import pandera as pa
from pandera.typing import Series


class DailyReturnsVolatilitySchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str] = pa.Field(nullable=False)
    daily_returns_volatility: Series[float]


class Volatility(pa.DataFrameModel):
    date_time: Series[datetime]
    volatility: Series[float]

    class Config:
        drop_invalid_rows = True


class InstrumentVolatilitySchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str] = pa.Field(nullable=False)
    instrument_volatility: Series[float]


class DailyVolNormalizedReturnsSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]


class DailyVolNormalisedPriceForAssetClassSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    asset_class: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]
