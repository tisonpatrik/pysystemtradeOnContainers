import asyncio
from asyncio import Task

import pandas as pd

from common.cqrs.api_queries.raw_data_queries.get_median_carry_for_asset_class import GetMedianCarryForAssetClassQuery
from common.cqrs.api_queries.raw_data_queries.get_raw_carry import GetRawCarryQuery
from common.cqrs.api_queries.raw_data_queries.get_smoothed_carry import GetSmoothedCarryQuery
from common.cqrs.cache_queries.median_carry_for_asset_class_cache import (
    GetMedianCarryForAssetClassCache,
    SetMedianCarryForAssetClassCache,
)
from common.cqrs.cache_queries.raw_carry_cache import GetRawCarryCache, SetRawCarryCache
from common.cqrs.cache_queries.smoothed_carry_cache import GetSmoothedCarryCache, SetSmoothedCarryCache
from common.cqrs.db_queries.get_carry_data import GetCarryDataQuery
from common.database.repository import PostgresClient
from common.http_client.rest_client import RestClient
from common.redis.redis_repository import RedisClient
from common.validation.carry_data import CarryData
from common.validation.median_carry_for_asset_class import MedianCarryForAssetClass
from common.validation.raw_carry import RawCarry
from common.validation.smoothed_carry import SmoothedCarry


class CarryClient:
    def __init__(self, postgres: PostgresClient, rest_client: RestClient, redis: RedisClient):
        self.rest_client = rest_client
        self.db_repository = postgres
        self.redis_repository = redis
        self.background_tasks: set[Task] = set()

    async def get_carry_data_async(self, symbol: str) -> pd.DataFrame:
        statement = GetCarryDataQuery(symbol=symbol)
        carry_data = await self.db_repository.fetch_many_async(statement)
        return CarryData.from_db_to_dataframe(carry_data)

    async def get_raw_carry_async(self, symbol: str) -> pd.Series:
        cache_statement = GetRawCarryCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return RawCarry.from_cache_to_series(cached_data)

        query = GetRawCarryQuery(symbol=symbol)
        data = await self.rest_client.get_data_async(query)
        carry = RawCarry.from_api_to_series(data)

        # Store the fetched data in Redis cache
        cache_set_statement = SetRawCarryCache(cache=carry, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        # Optional: add a callback to handle task completion
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return carry

    async def get_smoothed_carry_async(self, symbol: str) -> pd.Series:
        cache_statement = GetSmoothedCarryCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return SmoothedCarry.from_cache_to_series(cached_data)

        query = GetSmoothedCarryQuery(symbol=symbol)
        data = await self.rest_client.get_data_async(query)
        daily_roll = SmoothedCarry.from_api_to_series(data)

        # Store the fetched data in Redis cache
        cache_set_statement = SetSmoothedCarryCache(daily_roll=daily_roll, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        # Optional: add a callback to handle task completion
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return daily_roll

    async def get_median_carry_for_asset_class_async(self, symbol: str) -> pd.Series:
        cache_statement = GetMedianCarryForAssetClassCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return MedianCarryForAssetClass.from_cache_to_series(cached_data)

        query = GetMedianCarryForAssetClassQuery(symbol=symbol)
        data = await self.rest_client.get_data_async(query)
        daily_roll = MedianCarryForAssetClass.from_api_to_series(data)

        # Store the fetched data in Redis cache
        cache_set_statement = SetMedianCarryForAssetClassCache(daily_roll=daily_roll, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        # Optional: add a callback to handle task completion
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return daily_roll
