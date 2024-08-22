import pandas as pd
from common.src.cqrs.cache_queries.daily_prices_cache import GetDailyPricesCache, SetDailyPricesCache
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.cqrs.db_queries.get_raw_carry import GetRawCarryDataQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices
from common.src.validation.raw_carry import RawCarry
from common.src.utils.resampler import resample_prices_to_business_day_index

class PricesRepository:
    def __init__(self, db_repository: Repository, redis_repository: RedisRepository):
        self.repository = db_repository
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        self.logger.info(f"Fetching daily prices for {symbol}")
        cache_statement = GetDailyPricesCache(symbol)
        try:
            # Try to get the data from Redis cache
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                series = DailyPrices.from_cache_to_series(cached_data)
                return series

            # If cache miss, fetch from database
            statement = GetDailyPriceQuery(symbol=symbol)
            prices_data = await self.repository.fetch_many_async(statement)

            raw_prices = DailyPrices.from_db_to_series(prices_data)
            prices = resample_prices_to_business_day_index(raw_prices)

            # Store the fetched data in Redis cache
            cache_set_statement = SetDailyPricesCache(
                prices=prices,
                instrument_code=symbol
            )
            await self.redis_repository.set_cache(cache_set_statement)
            return prices
        except Exception as e:
            self.logger.error(f"Error when fetching daily prices for symbol {symbol}: {e}")
            raise

    async def get_denom_prices_async(self, symbol: str) -> pd.Series:
        self.logger.info(f"Fetching denom prices for {symbol}")
        statement = GetDenomPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            raw_prices = DenomPrices.from_db_to_series(prices_data)
            prices = resample_prices_to_business_day_index(raw_prices)
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching denom price for symbol {symbol}: {e}")
            raise

    async def get_raw_carry_async(self, symbol: str) -> pd.DataFrame:
        self.logger.info(f"Fetching raw carry data for {symbol}")
        statement = GetRawCarryDataQuery(symbol=symbol)
        try:
            carry_data = await self.repository.fetch_many_async(statement)
            carry = RawCarry.from_db_to_dataframe(carry_data)
            return carry
        except Exception as e:
            self.logger.error(f"Database error when fetching raw carry data for symbol {symbol}: {e}")
            raise
