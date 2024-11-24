from common.src.database.repository import PostgresClient
from common.src.redis.redis_repository import RedisClient
from raw_data.api.dependencies.handlers import (
    get_absolute_skew_deviation_handler,
    get_daily_returns_vol_handler,
    get_fx_prices_handler,
    get_instrument_currency_vol_handler,
    get_vol_attenuation_handler,
)
from raw_data.api.endpoints.absolute_skew_deviation import AbsoluteSkewDeviation
from raw_data.api.endpoints.daily_returns_vol import DailyReturnsVol
from raw_data.api.endpoints.fx_prices import FxPrices
from raw_data.api.endpoints.instrument_currency_vol import InstrumentCurrencyVol
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
