import pandas as pd

from common.src.cqrs.cache_queries.get_daily_vol_normalised_returns_cache import GetDailyvolNormalizedReturnsCache
from common.src.cqrs.cache_queries.set_daily_vol_normalised_returns_cache import SetDailyvolNormalizedReturnsCache
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.risk_client import RiskClient
from common.src.utils.convertors import convert_cache_to_series
from raw_data.src.services.daily_vol_normalised_returns_service import DailyVolNormalisedReturnsService
from raw_data.src.validation.daily_vol_normalized_returns import DailyvolNormalizedReturns


class DailyvolNormalizedReturnsHandler:
    def __init__(self, prices_repository: PricesRepository, risk_client: RiskClient, redis_repository: RedisRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.risk_client = risk_client
        self.redis_repository = redis_repository
        self.daily_vol_normalized_returns_service = DailyVolNormalisedReturnsService()

    async def get_daily_vol_normalised_returns(self, instrument_code: str) -> pd.Series:
        self.logger.info(f"Fetching Daily volatility normalised returns for {instrument_code}")
        cache_statement = GetDailyvolNormalizedReturnsCache(instrument_code)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                series = convert_cache_to_series(cached_data,
                    DailyvolNormalizedReturns, str(DailyvolNormalizedReturns.date_time), str(DailyvolNormalizedReturns.price))
                return series

            returnvol_data = await self.risk_client.get_daily_retuns_vol_async(instrument_code)
            prices = await self.prices_repository.get_daily_prices_async(instrument_code)
            norm_return = self.daily_vol_normalized_returns_service.get_daily_vol_normalised_returns(prices, returnvol_data)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyvolNormalizedReturnsCache(
                prices=prices,
                instrument_code=instrument_code
            )
            await self.redis_repository.set_cache(cache_set_statement)
            return norm_return
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching Daily volatility normalised returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")
