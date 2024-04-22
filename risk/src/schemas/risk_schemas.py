from datetime import datetime

from pandera import Check, DataFrameModel, Field
from pandera.dtypes import Timestamp
from pandera.typing import Index, Series


class DailyReturnsVolatilitySchema(DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str] = Field(nullable=False)
    vol_returns: Series[float]


class CumulativeVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    cum_vol_norm_returns: Series[float] = Field(nullable=True)

    class Config:
        strict = True
        drop_invalid_rows = True
        checks = [Check(lambda x: x >= 0)]


class Volatility(DataFrameModel):
    date_time: Series[datetime]
    volatility: Series[float]

    class Config:
        drop_invalid_rows = True


class InstrumentVolatilitySchema(DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str] = Field(nullable=False)
    instrument_volatility: Series[float]


class DailyVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    vol_normalized_returns: Series[float] = Field(nullable=True)


class DailyVolNormalisedPriceForAssetClassSchema(DataFrameModel):
    date_time: Series[datetime]
    asset_class: Series[str] = Field(nullable=False)
    vol_normalized_price_for_asset: Series[float]
