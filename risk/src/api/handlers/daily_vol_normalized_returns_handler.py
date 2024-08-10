import pandas as pd

from common.src.cqrs.cache_queries.daily_vol_normalized_returns_cache import (
    GetDailyvolNormalizedReturnsCache,
    SetDailyvolNormalizedReturnsCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_repository import PricesRepository
from risk.src.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from risk.src.services.daily_vol_normalized_returns_service import DailyVolnormalizedReturnsService
from risk.src.validation.daily_vol_normalized_returns import DailyvolNormalizedReturns


class DailyvolNormalizedReturnsHandler:
    def __init__(
        self,
        prices_repository: PricesRepository,
        daily_returns_vol_handler: DailyReturnsVolHandler,
        redis_repository: RedisRepository
    ):

        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.redis_repository = redis_repository
        self.daily_vol_normalized_returns_service = DailyVolnormalizedReturnsService()

    async def get_daily_vol_normalized_returns(self, instrument_code: str) -> pd.Series:
        self.logger.info(f"Fetching Daily volatility normalized returns for {instrument_code}")
        cache_statement = GetDailyvolNormalizedReturnsCache(instrument_code)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                series = DailyvolNormalizedReturns.from_api_to_series(cached_data)
                return series

            returnvol_data = await self.daily_returns_vol_handler.get_daily_returns_vol_async(instrument_code)
            prices = await self.prices_repository.get_daily_prices_async(instrument_code)
            norm_return = self.daily_vol_normalized_returns_service.get_daily_vol_normalized_returns(prices, returnvol_data)
            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyvolNormalizedReturnsCache(
                prices=prices,
                instrument_code=instrument_code
            )
            await self.redis_repository.set_cache(cache_set_statement)
            return norm_return
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching Daily volatility normalized returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")
