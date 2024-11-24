import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.cache_queries.cumulative_daily_vol_norm_returns_cache import (
    GetCumulativeDailyVolNormReturnsCache,
    SetCumulativeDailyVolNormReturnsCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisClient
from common.src.validation.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from raw_data.old_api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class CumulativeDailyVolNormReturnsHandler:
    def __init__(self, daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler, redis_repository: RedisClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.redis_repository = redis_repository
        self.background_tasks: set[Task] = set()

    async def get_cumulative_daily_vol_normalized_returns_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching cumulative daily vol normalized returns for asset class %s", symbol)
        cached_returns = await self._get_cached_returns(symbol)
        if cached_returns is not None:
            return cached_returns
        norm_returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns_async(symbol)
        returns = norm_returns.cumsum()
        self._cache_aggregated_returns(returns, symbol)
        return returns

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetCumulativeDailyVolNormReturnsCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return CumulativeDailyVolNormReturns.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, prices: pd.Series, symbol: str) -> None:
        cache_statement = SetCumulativeDailyVolNormReturnsCache(prices=prices, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
