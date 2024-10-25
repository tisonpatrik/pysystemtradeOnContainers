import asyncio

import pandas as pd

from common.src.cqrs.api_queries.get_median_carry_for_asset_class import GetMedianCarryForAssetClassQuery
from common.src.cqrs.api_queries.get_raw_carry import GetRawCarryQuery
from common.src.cqrs.api_queries.get_smoothed_carry import GetSmoothedCarryQuery
from common.src.cqrs.cache_queries.median_carry_for_asset_class_cache import (
    GetMedianCarryForAssetClassCache,
    SetMedianCarryForAssetClassCache,
)
from common.src.cqrs.cache_queries.raw_carry_cache import GetRawCarryCache, SetRawCarryCache
from common.src.cqrs.cache_queries.smoothed_carry_cache import GetSmoothedCarryCache, SetSmoothedCarryCache
from common.src.cqrs.db_queries.get_carry_data import GetCarryDataQuery
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.carry_data import CarryData
from common.src.validation.median_carry_for_asset_class import MedianCarryForAssetClass
from common.src.validation.raw_carry import RawCarry
from common.src.validation.smoothed_carry import SmoothedCarry


class CarryClient:
    def __init__(self, db_repository: Repository, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.db_repository = db_repository
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()
        self.background_tasks = set()

    async def get_carry_data_async(self, symbol: str) -> pd.DataFrame:
        statement = GetCarryDataQuery(symbol=symbol)
        try:
            carry_data = await self.db_repository.fetch_many_async(statement)
            return CarryData.from_db_to_dataframe(carry_data)
        except Exception:
            self.logger.exception("Database error when fetching raw carry data for symbol%s", symbol)
            raise

    async def get_raw_carry_async(self, symbol: str) -> pd.Series:
        cache_statement = GetRawCarryCache(symbol)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return RawCarry.from_cache_to_series(cached_data)

            query = GetRawCarryQuery(symbol=symbol)
            data = await self.client.get_data_async(query)
            daily_roll = RawCarry.from_api_to_series(data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetRawCarryCache(daily_roll=daily_roll, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return daily_roll
        except Exception:
            self.logger.exception("Error fetching raw carry for %s", symbol)
            raise

    async def get_smoothed_carry_async(self, symbol: str) -> pd.Series:
        cache_statement = GetSmoothedCarryCache(symbol)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return SmoothedCarry.from_cache_to_series(cached_data)

            query = GetSmoothedCarryQuery(symbol=symbol)
            data = await self.client.get_data_async(query)
            daily_roll = SmoothedCarry.from_api_to_series(data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetSmoothedCarryCache(daily_roll=daily_roll, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return daily_roll
        except Exception:
            self.logger.exception("Error fetching raw carry for %s", symbol)
            raise

    async def get_median_carry_for_asset_class_async(self, symbol: str) -> pd.Series:
        cache_statement = GetMedianCarryForAssetClassCache(symbol)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return MedianCarryForAssetClass.from_cache_to_series(cached_data)

            query = GetMedianCarryForAssetClassQuery(symbol=symbol)
            data = await self.client.get_data_async(query)
            daily_roll = MedianCarryForAssetClass.from_api_to_series(data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetMedianCarryForAssetClassCache(daily_roll=daily_roll, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return daily_roll
        except Exception:
            self.logger.exception("Error fetching raw carry for %s", symbol)
            raise
