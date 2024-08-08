import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from raw_data.src.services.cumulatve_daily_vol_normalized_returns_service import CumulativeDailyVolNormalizedReturnsService
from raw_data.src.services.normalised_price_for_asset_class_service import NormalisedPriceForAssetClassService
from raw_data.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler

class NormalizedPricesForAssetClassHandler:
    def __init__(
        self,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
        aggregated_returns_for_asset_class_handler: AggregatedReturnsForAssetClassHandler
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.aggregated_returns_for_asset_class_handler = aggregated_returns_for_asset_class_handler
        self.cumulatve_daily_vol_normalized_returns_service = CumulativeDailyVolNormalizedReturnsService()
        self.normalised_price_for_asset_class_service = NormalisedPriceForAssetClassService()

    async def get_normalized_price_for_asset_class_async(self, query: GetNormalizedPriceForAssetClassQuery) -> pd.Series:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {query}")
            aggregated_returns_for_asset_class = await self.aggregated_returns_for_asset_class_handler.get_aggregated_returns_for_asset_class_async(query.asset_class)
            normalised_price_for_asset_class = (
                self.cumulatve_daily_vol_normalized_returns_service.get_cumulative_daily_vol_normalised_returns(aggregated_returns_for_asset_class)
            )
            normalised_price_this_instrument = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(query.symbol)
            normalised_price_for_asset = self.normalised_price_for_asset_class_service.get_cumulative_daily_vol_normalised_returns(
                normalised_price_for_asset_class, normalised_price_this_instrument
            )
            return normalised_price_for_asset

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching normalied prices for asset class: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")
