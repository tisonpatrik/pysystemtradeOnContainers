import asyncio

import pandas as pd

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.api_queries.get_raw_carry import GetRawCarryQuery
from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.cqrs.cache_queries.raw_carry_cache import GetRawCarryCache, SetRawCarryCache
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_returns_vol import DailyReturnsVol
from common.src.validation.raw_carry import RawCarry


class RawDataClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_returns_vol_async(self, instrument_code: str) -> pd.Series:
        cache_statement = GetDailyReturnsVolCache(instrument_code)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyReturnsVol.from_cache_to_series(cached_data)

            query = GetDailyReturnsVolQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            vol = DailyReturnsVol.from_api_to_series(vol_data)

            cache_set_statement = SetDailyReturnsVolCache(vol=vol, instrument_code=instrument_code)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
            return vol
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", instrument_code)
            raise

    async def get_raw_carry_async(self, instrument_code: str) -> pd.Series:
        cache_statement = GetRawCarryCache(instrument_code)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return RawCarry.from_cache_to_series(cached_data)

            query = GetRawCarryQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            daily_roll = RawCarry.from_api_to_series(vol_data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetRawCarryCache(daily_roll=daily_roll, symbol=instrument_code)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
            return daily_roll
        except Exception:
            self.logger.exception("Error fetching raw carry for %s", instrument_code)
            raise
