import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.momentum_cache import GetMomentumCache, SetMomentumCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.momentum import MomentumService
from rules.src.validation.ewmac_signal import EwmacSignal


class MomentumHandler:
    def __init__(self, prices_repository: PricesClient, raw_data_client: RawDataClient, redis_repository: RedisRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client
        self.redis_repository = redis_repository
        self.momentum_service = MomentumService()
        self.background_tasks = set()

    async def get_momentum_async(self, symbol: str, Lfast: int) -> pd.Series:
        self.logger.info("Calculating Momentum rule for %s with Lfast %d", symbol, Lfast)
        cached_signal = await self._get_cached_signal(symbol, Lfast)
        if cached_signal is not None:
            return cached_signal
        daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
        daily_vol = await self.raw_data_client.get_daily_returns_vol_async(symbol)
        signal = self.momentum_service.calculate_ewmac(daily_prices, daily_vol, Lfast)
        self._cache_aggregated_signal(signal, symbol, Lfast)
        return signal

    async def _get_cached_signal(self, symbol: str, speed: int) -> pd.Series | None:
        cache_statement = GetMomentumCache(symbol, speed)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return EwmacSignal.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_signal(self, signal: pd.Series, symbol: str, speed: int) -> None:
        cache_statement = SetMomentumCache(signal=signal, symbol=symbol, speed=speed)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
