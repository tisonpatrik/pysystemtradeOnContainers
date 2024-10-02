import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.daily_prices_cache import GetDailyPricesCache, SetDailyPricesCache
from common.src.cqrs.db_queries.get_carry_data import GetCarryDataQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.utils.resampler import resample_prices_to_business_day_index
from common.src.validation.carry_data import CarryData
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices


class PricesRepository:
    def __init__(self, db_repository: Repository, redis_repository: RedisRepository):
        self.repository = db_repository
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching daily prices for %s", symbol)
        cache_statement = GetDailyPricesCache(symbol)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyPrices.from_cache_to_series(cached_data)

            # If cache miss, fetch from database
            statement = GetDailyPriceQuery(symbol=symbol)
            prices_data = await self.repository.fetch_many_async(statement)
            raw_prices = DailyPrices.from_db_to_series(prices_data)
            prices = resample_prices_to_business_day_index(raw_prices)

            # Store the fetched data in Redis cache in the background (fire-and-forget)
            cache_set_statement = SetDailyPricesCache(prices=prices, instrument_code=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))

            return prices
        except Exception:
            self.logger.exception("Error when fetching daily prices for symbol %s", symbol)
            raise

    async def get_denom_prices_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching denom prices for %s", symbol)
        statement = GetDenomPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            raw_prices = DenomPrices.from_db_to_series(prices_data)
            return resample_prices_to_business_day_index(raw_prices)
        except Exception:
            self.logger.exception("Database error when fetching denom price for symbol %s", symbol)
            raise

    async def get_raw_carry_async(self, symbol: str) -> pd.DataFrame:
        self.logger.info("Fetching raw carry data for %s", symbol)
        statement = GetCarryDataQuery(symbol=symbol)
        try:
            carry_data = await self.repository.fetch_many_async(statement)
            return CarryData.from_db_to_dataframe(carry_data)
        except Exception:
            self.logger.exception("Database error when fetching raw carry data for symbol%s", symbol)
            raise
