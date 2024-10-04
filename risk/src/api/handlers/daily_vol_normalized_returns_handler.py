import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.daily_vol_normalized_returns_cache import (
    GetDailyvolNormalizedReturnsCache,
    SetDailyvolNormalizedReturnsCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from common.src.validation.daily_vol_normalized_returns import DailyvolNormalizedReturns
from risk.src.services.daily_vol_normalized_returns_service import DailyVolnormalizedReturnsService


class DailyvolNormalizedReturnsHandler:
    def __init__(self, prices_repository: PricesRepository, raw_data_client: RawDataClient, redis_repository: RedisRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client
        self.redis_repository = redis_repository
        self.daily_vol_normalized_returns_service = DailyVolnormalizedReturnsService()

    async def get_daily_vol_normalized_returns_async(self, instrument_code: str) -> pd.Series:
        self.logger.info("Fetching Daily volatility normalized returns for %s", instrument_code)
        cache_statement = GetDailyvolNormalizedReturnsCache(instrument_code)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyvolNormalizedReturns.from_cache_to_series(cached_data)

            returnvol_data = await self.raw_data_client.get_daily_returns_vol_async(instrument_code)
            prices = await self.prices_repository.get_daily_prices_async(instrument_code)
            norm_return = self.daily_vol_normalized_returns_service.get_daily_vol_normalized_returns(prices, returnvol_data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyvolNormalizedReturnsCache(prices=prices, symbol=instrument_code)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
            return norm_return
        except Exception:
            self.logger.exception("Unexpected error occurred while fetching Daily volatility normalized returns")
            raise
