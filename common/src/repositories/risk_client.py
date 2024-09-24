import asyncio

import httpx
import pandas as pd

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.daily_returns_vol import DailyReturnsVol
from common.src.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass


class RiskClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_retuns_vol_async(self, instrument_code: str) -> pd.Series:
        self.logger.info("Fetching daily returns vol rate for %s", instrument_code)

        cache_statement = GetDailyReturnsVolCache(instrument_code)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return DailyReturnsVol.from_cache_to_series(cached_data)

            query = GetDailyReturnsVolQuery(symbol=instrument_code)
            vol_data = await self.client.get_data_async(query)
            vol = DailyReturnsVol.from_api_to_series(vol_data)

            cache_set_statement = SetDailyReturnsVolCache(vol=vol, instrument_code=instrument_code)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

            # Optional: add a callback to handle task completion
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))
            return vol
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", instrument_code)
            raise

    async def get_normalized_prices_for_asset_class_async(self, symbol: str, asset_class: str) -> pd.Series:
        query = GetNormalizedPriceForAssetClassQuery(symbol=symbol, asset_class=asset_class)
        try:
            vol_data = await self.client.get_data_async(query)
            return NormalizedPricesForAssetClass.from_api_to_series(vol_data)

        except httpx.HTTPStatusError as http_exc:
            self.logger.exception(
                "HTTP error occurred while fetching data for %s: %s - %s",
                symbol,
                http_exc.response.status_code,
                http_exc.response.text,
            )
            raise
        except httpx.RequestError:
            self.logger.exception("Request error occurred while fetching data for %s", symbol)
            raise
        except Exception:
            self.logger.exception("Error fetching daily returns vol rate for %s", symbol)
            raise
