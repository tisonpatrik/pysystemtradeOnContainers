import pandas as pd

from common.src.cqrs.cache_queries.get_daily_prices_cache import GetDailyPricesCache
from common.src.cqrs.cache_queries.set_daily_prices_cache import SetDailyPricesCache
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.utils.convertors import list_to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices


class PricesRepository:
    def __init__(self, db_repository: Repository, redis_repository: RedisRepository):
        self.repository = db_repository
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDailyPricesCache(symbol)

        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data:
                self.logger.info(f"Cache hit for symbol {symbol}")
                return pd.Series(cached_data)

            # If cache miss, fetch from database
            statement = GetDailyPriceQuery(symbol=symbol)
            prices_data = await self.repository.fetch_many_async(statement)
            prices = list_to_series(prices_data, DailyPrices, str(DailyPrices.date_time), str(DailyPrices.price))

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyPricesCache(
                prices=prices,
                instrument_code=symbol
            )
            await self.redis_repository.set_cache(cache_set_statement)

            return prices
        except Exception as e:
            self.logger.error(f"Error when fetching daily prices for symbol {symbol}: {e}")
            raise

    async def get_denom_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDenomPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = list_to_series(prices_data, DenomPrices, DenomPrices.date_time, DenomPrices.price)  # type: ignore[arg-type]
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching denom price for symbol {symbol}: {e}")
            raise
