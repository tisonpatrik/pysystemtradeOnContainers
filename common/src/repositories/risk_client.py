import httpx
import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass


class RiskClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.logger = AppLogger.get_instance().get_logger()

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
