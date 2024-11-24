import asyncio
from asyncio import Task

import pandas as pd

from common.src.clients.prices_client import PricesClient
from common.src.cqrs.cache_queries.daily_percentage_vol_cache import (
    GetDailyPercentageVolCache,
    SetDailyPercentageVolCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisClient
from common.src.validation.daily_percentage_vol import DailyPercentageVo
from raw_data.src.raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler


class DailyPercentageVolatilityHandler:
    def __init__(
        self,
        prices_client: PricesClient,
        redis_repository: RedisClient,
        daily_returns_vol_handler: DailyReturnsVolHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_client = prices_client
        self.redis_repository = redis_repository
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.background_tasks: set[Task] = set()

    async def get_daily_percentage_volatility_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching daily percentage volatility for %s.", symbol)
        cached_volatility = await self._get_cached_volatility(symbol)
        if cached_volatility is not None:
            return cached_volatility
        denom_prices = await self.prices_client.get_denom_prices_async(symbol)
        daily_returns_vol = await self.daily_returns_vol_handler.get_daily_returns_vol_async(symbol)
        (denom_price, return_vol) = denom_prices.align(daily_returns_vol, join="right")
        daily_volatility = 100.0 * (return_vol / denom_price.ffill().abs())
        self._cache_aggregated_volatility(daily_volatility, symbol)
        return daily_volatility

    async def _get_cached_volatility(self, symbol: str) -> pd.Series | None:
        cache_statement = GetDailyPercentageVolCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return DailyPercentageVo.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_volatility(self, daily_volatility: pd.Series, symbol: str) -> None:
        cache_statement = SetDailyPercentageVolCache(vol=daily_volatility, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
