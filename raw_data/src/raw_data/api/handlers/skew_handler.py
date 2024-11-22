import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.cache_queries.negskew_cache import GetNegSkewCache, SetNegSkewCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisClient
from common.src.validation.negskew import NegSkew
from raw_data.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.services.skew_service import SkewService


class SkewHandler:
    def __init__(self, daily_percentage_returns_handler: DailyPercentageReturnsHandler, redis: RedisClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_returns_handler = daily_percentage_returns_handler
        self.redis_repository = redis
        self.skew_service = SkewService()
        self.background_tasks: set[Task] = set()

    async def get_skew_async(self, symbol: str, lookback: int) -> pd.Series:
        self.logger.info("Fetching skew for symbol %s", symbol)
        perc_returns = await self.daily_percentage_returns_handler.get_daily_percentage_returns_async(symbol)
        return self.skew_service.calculate_skew(perc_returns, lookback)

    async def get_neg_skew_async(self, symbol: str, lookback: int) -> pd.Series:
        self.logger.info("Fetching negative skew for symbol %s", symbol)
        cached_returns = await self._get_cached_returns(symbol=symbol, lookback=lookback)
        if cached_returns is not None:
            return cached_returns
        skew = await self.get_skew_async(symbol, lookback)
        negskew = -skew
        self._cache_aggregated_returns(negskew=negskew, symbol=symbol, lookback=lookback)
        return negskew

    async def _get_cached_returns(self, symbol: str, lookback: int) -> pd.Series | None:
        cache_statement = GetNegSkewCache(symbol, lookback)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return NegSkew.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, negskew: pd.Series, symbol: str, lookback: int) -> None:
        cache_statement = SetNegSkewCache(negskew=negskew, symbol=symbol, lookback=lookback)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
