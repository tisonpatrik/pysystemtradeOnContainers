import asyncio
from asyncio import Task

import pandas as pd
from common.cqrs.cache_queries.daily_vol_normalized_returns_cache import (
    GetDailyvolNormalizedReturnsCache,
    SetDailyvolNormalizedReturnsCache,
)
from common.logging.logger import AppLogger
from common.redis.redis_repository import RedisClient

from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.services.daily_vol_normalized_returns_service import DailyVolnormalizedReturnsService
from raw_data.validation.daily_vol_normalized_returns import DailyVolNormalizedReturns


class DailyVolNormalizedReturnsHandler:
    def __init__(
        self,
        daily_returns_vol_handler: DailyReturnsVolHandler,
        redis: RedisClient,
        daily_returns_handler: DailyReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.redis_repository = redis
        self.daily_returns_handler = daily_returns_handler

        self.daily_vol_normalized_returns_service = DailyVolnormalizedReturnsService()
        self.background_tasks: set[Task] = set()

    async def get_daily_vol_normalized_returns_async(self, symbol: str) -> pd.Series:
        self.logger.info('Fetching Daily volatility normalized returns for %s', symbol)
        cached_returns = await self._get_cached_returns(symbol)
        if cached_returns is not None:
            return cached_returns
        returnvol_data = await self.daily_returns_vol_handler.get_daily_returns_vol_async(symbol)
        dailyreturns = await self.daily_returns_handler.get_daily_returns_async(symbol)
        returns = self.daily_vol_normalized_returns_service.calculate_daily_vol_normalized_returns(returnvol_data, dailyreturns)
        self._cache_aggregated_returns(returns, symbol)
        return returns

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetDailyvolNormalizedReturnsCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info('Cache hit for asset class: %s', symbol)
            return DailyVolNormalizedReturns.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, returns: pd.Series, symbol: str) -> None:
        cache_statement = SetDailyvolNormalizedReturnsCache(returns=returns, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)