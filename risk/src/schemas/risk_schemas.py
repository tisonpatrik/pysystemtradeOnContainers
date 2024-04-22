from pandera import Check, DataFrameModel, Field
from pandera.dtypes import Timestamp
from pandera.typing import Index, Series


class CumulativeVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    cum_vol_norm_returns: Series[float] = Field(nullable=True)

    class Config:
        strict = True


class DailyVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(nullable=True)
    vol_normalized_returns: Series[float] = Field(nullable=True)

    class Config:
        strict = True


class DailyReturnsVolatilitySchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    symbol: Series[str] = Field(nullable=False)
    vol_returns: Series[float]


class Volatility(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    volatility: Series[float]

    class Config:
        strict = True


class InstrumentVolatilitySchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    symbol: Series[str] = Field(nullable=True, regex=True)
    instrument_volatility: Series[float]


class DailyVolNormalisedPriceForAssetClassSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    asset_class: Series[str] = Field(nullable=False)
    vol_normalized_price_for_asset: Series[float]
