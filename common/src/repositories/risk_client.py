import pandas as pd
from fastapi import HTTPException

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.utils.convertors import convert_cache_to_series, from_api_to_series
from common.src.validation.daily_returns_vol import DailyReturnsVol


class RiskClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_retuns_vol_async(self, instrument_code: str) -> pd.Series:
        self.logger.info(f"Fetching daily returns vol rate for {instrument_code}")

        cache_statement = GetDailyReturnsVolCache(instrument_code)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                series = convert_cache_to_series(cached_data, DailyReturnsVol,
                    str(DailyReturnsVol.date_time), str(DailyReturnsVol.vol))
                return series

            query = GetDailyReturnsVolQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            vol = from_api_to_series(vol_data, DailyReturnsVol,
                DailyReturnsVol.date_time, DailyReturnsVol.vol)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyReturnsVolCache(
                vol=vol,
                instrument_code=instrument_code
            )
            await self.redis_repository.set_cache(cache_set_statement)
            return vol
        except Exception as e:
            self.logger.error(f"Error fetching daily returns vol rate for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching daily returns vol rate")
