import pandera as pa
from pandera.typing import Series


class DailyReturnsVolatilitySchema(pa.SeriesSchema):
    unix_date_time: Series[int]
    symbol: Series[str] = pa.Field(coerce=True, checks=pa.Check.str_length(0, 50))
    daily_returns_volatility: Series[float]


class InstrumentVolatilitySchema(pa.SeriesSchema):
    unix_date_time: Series[int]
    symbol: Series[str] = pa.Field(coerce=True, checks=pa.Check.str_length(0, 50))
    instrument_volatility: Series[float]


class DailyVolNormalizedReturnsSchema(pa.SeriesSchema):
    unix_date_time: Series[int]
    symbol: Series[str] = pa.Field(coerce=True, checks=pa.Check.str_length(0, 50))
    normalized_volatility: Series[float]


class DailyVolNormalisedPriceForAssetClassSchema(pa.SeriesSchema):
    unix_date_time: Series[int]
    asset_class: Series[str] = pa.Field(coerce=True, checks=pa.Check.str_length(0, 50))
    normalized_volatility: Series[float]
