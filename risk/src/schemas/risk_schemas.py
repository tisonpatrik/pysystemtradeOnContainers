import pandas as pd
import pandera as pa
from pandera.typing import Series


class DailyReturnsVolatilitySchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = pa.Field(nullable=False)
    daily_returns_volatility: Series[float]


class InstrumentVolatilitySchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = pa.Field(nullable=False)
    instrument_volatility: Series[float]


class DailyVolNormalizedReturnsSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    symbol: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]


class DailyVolNormalisedPriceForAssetClassSchema(pa.DataFrameModel):
    date_time: Series[pd.Timestamp]
    asset_class: Series[str] = pa.Field(nullable=False)
    normalized_volatility: Series[float]
