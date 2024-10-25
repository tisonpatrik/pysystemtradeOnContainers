import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.daily_returns_cache import GetDailyReturnsCache, SetDailyReturnsCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_client import PricesClient
from common.src.validation.daily_returns import DailyReturns


class DailyReturnsHandler:
    def __init__(self, prices_repository: PricesClient, redis_repository: RedisRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.redis_repository = redis_repository
        self.background_tasks = set()

    async def get_daily_returns_async(self, symbol: str) -> pd.Series:
        try:
            cached_returns = await self._get_cached_returns(symbol)
            if cached_returns is not None:
                return cached_returns
            prices = await self.prices_repository.get_daily_prices_async(symbol)
            returns = prices.diff()
            self._cache_aggregated_returns(returns, symbol)
            return returns
        except Exception:
            self.logger.exception("Error in processing daily returns")
            raise

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetDailyReturnsCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return DailyReturns.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, returns: pd.Series, symbol: str) -> None:
        cache_statement = SetDailyReturnsCache(returns=returns, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
