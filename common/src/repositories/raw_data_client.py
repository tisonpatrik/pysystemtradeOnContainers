import asyncio

import pandas as pd

from common.src.cqrs.api_queries.get_daily_annualised_roll import GetDailyAnnualisedRollQuery
from common.src.cqrs.cache_queries.daily_annualised_roll_cache import GetDailyAnnualisedRollCache, SetDailyAnnualisedRollCache
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_annualised_roll import DailyAnnualisedRoll


class RawDataClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_annualised_roll_async(self, instrument_code: str) -> pd.Series:
        self.logger.info("Fetching daily annualised roll for, %s", instrument_code)

        cache_statement = GetDailyAnnualisedRollCache(instrument_code)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyAnnualisedRoll.from_cache_to_series(cached_data)

            query = GetDailyAnnualisedRollQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            daily_roll = DailyAnnualisedRoll.from_api_to_series(vol_data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyAnnualisedRollCache(daily_roll=daily_roll, symbol=instrument_code)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
            return daily_roll
        except Exception:
            self.logger.exception("Error fetching daily annualised roll for %s", instrument_code)
            raise
