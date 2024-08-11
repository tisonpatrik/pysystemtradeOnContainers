import pandas as pd
from fastapi import HTTPException

from common.src.cqrs.cache_queries.daily_annualised_roll_cache import GetDailyAnnualisedRollCache, SetDailyAnnualisedRollCache
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_annualised_roll import DailyAnnualisedRoll
from common.src.cqrs.api_queries.get_daily_annualised_roll import GetDailyAnnualisedRollQuery

class RawDataClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_annualised_roll_async(self, instrument_code: str) -> pd.Series:
        self.logger.info(f"Fetching daily annualised roll for {instrument_code}")

        cache_statement = GetDailyAnnualisedRollCache(instrument_code)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                series = DailyAnnualisedRoll.from_cache_to_series(cached_data)
                return series

            query = GetDailyAnnualisedRollQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            daily_roll = DailyAnnualisedRoll.from_api_to_series(vol_data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyAnnualisedRollCache(
                daily_roll=daily_roll,
                symbol=instrument_code
            )
            await self.redis_repository.set_cache(cache_set_statement)
            return daily_roll
        except Exception as e:
            self.logger.error(f"Error fetching daily annualised roll for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching daily annualised roll for")
