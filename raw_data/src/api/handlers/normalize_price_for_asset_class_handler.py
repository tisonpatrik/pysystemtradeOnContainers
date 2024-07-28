import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.cqrs.db_queries.get_asset_class import GetAssetClass
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.asset_class import AssetClass
from raw_data.src.services.normalised_price_for_asset_class_service import NormalisedPriceForAssetClassService


class NormalizedPriceForAssetClassHandler:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.fx_prices_service = NormalisedPriceForAssetClassService()

    async def get_normalized_price_for_asset_class_async(
        self, get_normalized_price_query: NormalizedPriceForAssetClassQuery
    ) -> pd.DataFrame:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {get_normalized_price_query}")
            asset_class = await self._get_asset_class_async(get_normalized_price_query.symbol)
            print(asset_class)
            return pd.DataFrame()
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching FX prices: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    async def _get_asset_class_async(self, symbol: str) -> AssetClass:
        statement = GetAssetClass(symbol=symbol)
        try:
            asset_class_data = await self.repository.fetch_item_async(statement)
            asset_class = to_pydantic(asset_class_data, AssetClass)
            if asset_class is None:
                raise ValueError(f"No data found for symbol {symbol}")
            return asset_class
        except Exception as e:
            self.logger.error(f"Database error when fetching asset class for symbol {symbol}: {e}")
            raise
