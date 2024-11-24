import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.cache_queries.raw_carry_cache import GetRawCarryCache, SetRawCarryCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisClient
from common.src.validation.raw_carry import RawCarry
from raw_data.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.services.raw_carry_service import RawCarryService
from raw_data.utils.carry import get_raw_carry


class RawCarryHandler:
    def __init__(
        self,
        redis: RedisClient,
        daily_annualised_roll_handler: DailyAnnualisedRollHandler,
        daily_returns_vol_handler: DailyReturnsVolHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.redis_repository = redis
        self.daily_annualised_roll_handler = daily_annualised_roll_handler
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.raw_carry_service = RawCarryService()
        self.background_tasks: set[Task] = set()

    async def get_raw_carry_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching Raw Carry for symbol %s", symbol)
        cache = await self._get_cache(symbol)
        if cache is not None:
            return cache
        annroll = await self.daily_annualised_roll_handler.get_daily_annualised_roll_async(symbol)
        daily_returns_vol = await self.daily_returns_vol_handler.get_daily_returns_vol_async(symbol)
        results = get_raw_carry(annroll, daily_returns_vol)
        self._set_cache_results(results, symbol)
        return results

    async def _get_cache(self, symbol: str) -> pd.Series | None:
        cache_statement = GetRawCarryCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return RawCarry.from_cache_to_series(cached_data)
        return None

    def _set_cache_results(self, returns: pd.Series, symbol: str) -> None:
        cache_statement = SetRawCarryCache(cache=returns, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
