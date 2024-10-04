import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.daily_vol_normalized_returns_cache import (
    GetDailyvolNormalizedReturnsCache,
    SetDailyvolNormalizedReturnsCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from risk.src.services.daily_vol_normalized_returns_service import DailyVolnormalizedReturnsService
from risk.src.validation.daily_vol_normalized_returns import DailyVolNormalizedReturns


class DailyvolNormalizedReturnsHandler:
    def __init__(self, prices_repository: PricesClient, raw_data_client: RawDataClient, redis_repository: RedisRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client
        self.redis_repository = redis_repository
        self.daily_vol_normalized_returns_service = DailyVolnormalizedReturnsService()

    async def get_daily_vol_normalized_returns_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching Daily volatility normalized returns for %s", symbol)
        try:
            cached_returns = await self._get_cached_returns(symbol)
            if cached_returns is not None:
                return cached_returns
            returnvol_data = await self.raw_data_client.get_daily_returns_vol_async(symbol)
            prices = await self.prices_repository.get_daily_prices_async(symbol)
            returns = self.daily_vol_normalized_returns_service.get_daily_vol_normalized_returns(prices, returnvol_data)
            self._cache_aggregated_returns(returns, symbol)
            return returns
        except Exception:
            self.logger.exception("Unexpected error occurred while fetching Daily volatility normalized returns")
            raise

    async def _get_cached_returns(self, symbol: str) -> pd.Series | None:
        cache_statement = GetDailyvolNormalizedReturnsCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            self.logger.info("Cache hit for asset class: %s", symbol)
            return DailyVolNormalizedReturns.from_cache_to_series(cached_data)
        return None

    def _cache_aggregated_returns(self, returns: pd.Series, symbol: str) -> None:
        cache_statement = SetDailyvolNormalizedReturnsCache(returns=returns, asset_class=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_statement))
        cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
