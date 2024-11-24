from common.src.database.repository import PostgresClient
from common.src.redis.redis_repository import RedisClient
from raw_data.api.dependencies.handlers import get_absolute_skew_deviation_handler, get_fx_prices_handler
from raw_data.api.endpoints.absolute_skew_deviation import AbsoluteSkewDeviation
from raw_data.api.endpoints.fx_prices import FxPrices


def get_absolute_skew_deviation(postgres: PostgresClient, redis: RedisClient) -> AbsoluteSkewDeviation:
    handler = get_absolute_skew_deviation_handler(postgres=postgres, redis=redis)
    return AbsoluteSkewDeviation(absolute_skew_deviation_handler=handler)


def get_fx_prices(postgres: PostgresClient, redis: RedisClient) -> FxPrices:
    handler = get_fx_prices_handler(postgres=postgres, redis=redis)
    return FxPrices(fx_prices_handler=handler)
