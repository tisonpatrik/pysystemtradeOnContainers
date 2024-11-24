import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.cache_queries.vol_attenuation_cache import GetVolAttenuationCache, SetVolAttenuationCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisClient
from common.src.validation.vol_attenuation import VolAttenuation
from raw_data.old_api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.services.vol_attenuation_service import VolAttenuationService


class VolAttenuationHandler:
    def __init__(self, daily_percentage_volatility_handler: DailyPercentageVolatilityHandler, redis_repository: RedisClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_volatility_handler = daily_percentage_volatility_handler
        self.redis_repository = redis_repository
        self.vol_attenuation_service = VolAttenuationService()
        self.background_tasks: set[Task] = set()

    async def get_vol_attenuation_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching volatility attenuation for symbol %s", symbol)
        cached_returns = await self._get_cached_returns(symbol)
        if cached_returns is not None:
            return cached_returns
        daily_vol = await self.daily_percentage_volatility_handler.get_daily_percentage_volatility_async(symbol)
        ten_year_vol = daily_vol.rolling(2500, min_periods=10).mean()
        normalised_vol = daily_vol / ten_year_vol
        vol_attenuation = self.vol_attenuation_service.calculate_vol_attenuation(normalised_vol)

        self._cache_aggregated_returns(vol_attenuation, symbol)
        return vol_attenuation

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetVolAttenuationCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return VolAttenuation.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, vol_attenuation: pd.Series, symbol: str) -> None:
        cache_statement = SetVolAttenuationCache(values=vol_attenuation, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
