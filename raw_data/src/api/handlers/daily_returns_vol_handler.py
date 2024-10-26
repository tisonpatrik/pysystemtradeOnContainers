import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_client import PricesClient
from common.src.validation.daily_returns_vol import DailyReturnsVol
from raw_data.src.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolHandler:
    def __init__(self, prices_repository: PricesClient, redis_repository: RedisRepository, daily_returns_handler: DailyReturnsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.redis_repository = redis_repository
        self.daily_returns_handler = daily_returns_handler
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.background_tasks = set()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching daily returns volatility for %s.", symbol)
        cached_returns = await self._get_cached_returns(symbol)
        if cached_returns is not None:
            return cached_returns
        daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
        daily_returns = await self.daily_returns_handler.get_daily_returns_async(symbol)
        returns = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices, daily_returns)
        self._cache_aggregated_returns(returns, symbol)
        return returns

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetDailyReturnsVolCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return DailyReturnsVol.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, vol: pd.Series, symbol: str) -> None:
        cache_statement = SetDailyReturnsVolCache(vol=vol, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
