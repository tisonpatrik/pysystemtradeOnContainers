import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.cache_queries.daily_prices_cache import GetDailyPricesCache, SetDailyPricesCache
from common.src.cqrs.cache_queries.denom_prices_cache import GetDenomPricesCache, SetDenomPricesCache
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.cqrs.db_queries.get_fx_rates import GetFxRatesQuery
from common.src.database.repository import PostgresClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices
from common.src.validation.fx_rates import FxRates


class PricesClient:
    def __init__(self, db_repository: PostgresClient, redis_repository: RedisRepository):
        self.db_repository = db_repository
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()
        self.background_tasks: set[Task] = set()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDailyPricesCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return DailyPrices.from_cache_to_series(cached_data)

        # If cache miss, fetch from database
        statement = GetDailyPriceQuery(symbol=symbol)
        prices_data = await self.db_repository.fetch_many_async(statement)
        if not prices_data:
            raise ValueError("The provided data list is empty.")
        prices = DailyPrices.from_db_to_series(prices_data)

        # Store the fetched data in Redis cache in the background (fire-and-forget)
        cache_set_statement = SetDailyPricesCache(prices=prices, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return prices

    async def get_denom_prices_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDenomPricesCache(symbol)
        # Try to get the data from Redis cache
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return DenomPrices.from_cache_to_series(cached_data)
        # If cache miss, fetch from database
        statement = GetDenomPriceQuery(symbol=symbol)
        prices_data = await self.db_repository.fetch_many_async(statement)
        if not prices_data:
            raise ValueError("There are no data for symbol: %s.", symbol)
        prices = DenomPrices.from_db_to_series(prices_data)

        # Store the fetched data in Redis cache in the background (fire-and-forget)
        cache_set_statement = SetDenomPricesCache(prices=prices, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)

        return prices

    async def get_fx_rates_async(self, instrument_currency: str, conversion_currency: str) -> pd.Series:
        symbol = f"{instrument_currency}{conversion_currency}"
        statement = GetFxRatesQuery(symbol=symbol)
        rates_data = await self.db_repository.fetch_many_async(statement)
        if not rates_data:
            raise ValueError(f"There are no data for FX symbol: {symbol}.")
        return FxRates.from_db_to_series(rates_data)
