import asyncio

import pandas as pd

from common.src.cqrs.api_queries.get_absolute_skew_deviation import GetAbsoluteSkewDeviationQuery
from common.src.cqrs.api_queries.get_cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturnsQuery
from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.api_queries.get_normalized_price_for_asset_class import GetNormalizedPriceForAssetClassQuery
from common.src.cqrs.cache_queries.cumulative_daily_vol_norm_returns_cache import (
    GetCumulativeDailyVolNormReturnsCache,
    SetCumulativeDailyVolNormReturnsCache,
)
from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.cqrs.cache_queries.normalized_price_for_asset_class_cache import (
    GetNormalizedPriceForAssetClassCache,
    SetNormalizedPriceForAssetClassCache,
)
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.absolute_skew_deviation import AbsoluteSkewDeviation
from common.src.validation.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from common.src.validation.daily_returns_vol import DailyReturnsVol
from common.src.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass


class RawDataClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()
        self.background_tasks = set()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDailyReturnsVolCache(symbol)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyReturnsVol.from_cache_to_series(cached_data)

            query = GetDailyReturnsVolQuery(symbol=symbol)
            vol_data = await self.client.get_data_async(query)
            vol = DailyReturnsVol.from_api_to_series(vol_data)

            cache_set_statement = SetDailyReturnsVolCache(vol=vol, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return vol
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", symbol)
            raise

    async def get_normalized_prices_for_asset_class_async(self, symbol: str) -> pd.Series:
        cache_statement = GetNormalizedPriceForAssetClassCache(symbol)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return NormalizedPricesForAssetClass.from_cache_to_series(cached_data)
            query = GetNormalizedPriceForAssetClassQuery(symbol=symbol)
            raw_data = await self.client.get_data_async(query)
            data = NormalizedPricesForAssetClass.from_api_to_series(raw_data)
            cache_set_statement = SetNormalizedPriceForAssetClassCache(prices=data, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return data
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", symbol)
            raise

    async def get_cumulative_daily_vol_normalised_returns_async(self, symbol: str) -> pd.Series:
        cache_statement = GetCumulativeDailyVolNormReturnsCache(symbol)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return CumulativeDailyVolNormReturns.from_cache_to_series(cached_data)
            query = CumulativeDailyVolNormReturnsQuery(symbol=symbol)
            raw_data = await self.client.get_data_async(query)
            data = CumulativeDailyVolNormReturns.from_api_to_series(raw_data)
            cache_set_statement = SetCumulativeDailyVolNormReturnsCache(prices=data, symbol=symbol)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            self.background_tasks.add(cache_task)
            cache_task.add_done_callback(self.background_tasks.discard)
            return data
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", symbol)
            raise

    async def absolute_skew_deviation_async(self, symbol: str, lookback: int) -> pd.Series:
        query = GetAbsoluteSkewDeviationQuery(symbol=symbol, lookback=lookback)
        raw_data = await self.client.get_data_async(query)
        return AbsoluteSkewDeviation.from_api_to_series(raw_data)
