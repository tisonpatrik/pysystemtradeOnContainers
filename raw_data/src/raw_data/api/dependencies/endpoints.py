from common.src.database.repository import PostgresClient
from common.src.redis.redis_repository import RedisClient
from raw_data.api.dependencies.handlers import (
    get_absolute_skew_deviation_handler,
    get_cumulative_daily_vol_norm_returns_handler,
    get_daily_returns_vol_handler,
    get_fx_prices_handler,
    get_instrument_currency_vol_handler,
    get_median_carry_for_asset_class_handler,
    get_raw_carry_handler,
    get_relative_skew_deviation_handler,
    get_vol_attenuation_handler,
)
from raw_data.api.endpoints.absolute_skew_deviation import AbsoluteSkewDeviation
from raw_data.api.endpoints.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from raw_data.api.endpoints.daily_returns_vol import DailyReturnsVol
from raw_data.api.endpoints.fx_prices import FxPrices
from raw_data.api.endpoints.instrument_currency_vol import InstrumentCurrencyVol
from raw_data.api.endpoints.median_carry_for_asset_class import MedianCarryForAssetClass
from raw_data.api.endpoints.raw_carry import RawCarry
from raw_data.api.endpoints.relative_skew_deviation import RelativeSkewDeviation
from raw_data.api.endpoints.vol_attenuation import VolAttenuation


def get_absolute_skew_deviation(postgres: PostgresClient, redis: RedisClient) -> AbsoluteSkewDeviation:
    handler = get_absolute_skew_deviation_handler(postgres=postgres, redis=redis)
    return AbsoluteSkewDeviation(absolute_skew_deviation_handler=handler)


def get_fx_prices(postgres: PostgresClient, redis: RedisClient) -> FxPrices:
    handler = get_fx_prices_handler(postgres=postgres, redis=redis)
    return FxPrices(fx_prices_handler=handler)


def get_daily_returns_vol(postgres: PostgresClient, redis: RedisClient) -> DailyReturnsVol:
    handler = get_daily_returns_vol_handler(postgres=postgres, redis=redis)
    return DailyReturnsVol(daily_returns_vol_handler=handler)


def get_instrument_currency_vol(postgres: PostgresClient, redis: RedisClient) -> InstrumentCurrencyVol:
    handler = get_instrument_currency_vol_handler(postgres=postgres, redis=redis)
    return InstrumentCurrencyVol(instrument_currency_vol_handler=handler)


def get_vol_attenuation(postgres: PostgresClient, redis: RedisClient) -> VolAttenuation:
    handler = get_vol_attenuation_handler(postgres=postgres, redis=redis)
    return VolAttenuation(vol_attenuation_handler=handler)


def get_relative_skew_deviation(postgres: PostgresClient, redis: RedisClient) -> RelativeSkewDeviation:
    handler = get_relative_skew_deviation_handler(postgres=postgres, redis=redis)
    return RelativeSkewDeviation(relative_skew_deviation_handler=handler)


def get_cumulative_daily_vol_norm_returns(postgres: PostgresClient, redis: RedisClient) -> CumulativeDailyVolNormReturns:  # noqa: F821
    handler = get_cumulative_daily_vol_norm_returns_handler(postgres=postgres, redis=redis)
    return CumulativeDailyVolNormReturns(cumulative_daily_vol_norm_returns_handler=handler)


def get_raw_carry(postgres: PostgresClient, redis: RedisClient) -> RawCarry:
    handler = get_raw_carry_handler(postgres=postgres, redis=redis)
    return RawCarry(raw_carry_handler=handler)


def get_median_carry_for_asset_class(postgres: PostgresClient, redis: RedisClient) -> MedianCarryForAssetClass:
    handler = get_median_carry_for_asset_class_handler(postgres=postgres, redis=redis)
    return MedianCarryForAssetClass(median_carry_for_asset_class_handler=handler)
