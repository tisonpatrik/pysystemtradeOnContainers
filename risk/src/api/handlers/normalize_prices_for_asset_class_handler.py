import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from risk.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from risk.src.services.cumulatve_daily_vol_normalized_returns_service import CumulativeDailyVolNormalizedReturnsService
from risk.src.services.normalized_price_for_asset_class_service import normalizedPriceForAssetClassService


class NormalizedPricesForAssetClassHandler:
    def __init__(
        self,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
        aggregated_returns_for_asset_class_handler: AggregatedReturnsForAssetClassHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.aggregated_returns_for_asset_class_handler = aggregated_returns_for_asset_class_handler
        self.cum_daily_vol_norm_returns_service = CumulativeDailyVolNormalizedReturnsService()
        self.normalized_price_for_asset_class_service = normalizedPriceForAssetClassService()

    async def get_normalized_price_for_asset_class_async(self, query: GetNormalizedPriceForAssetClassQuery) -> pd.Series:
        try:
            self.logger.info("Fetching normalized prices for asset class %s", query)
            aggregated_returns_for_asset_class = (
                await self.aggregated_returns_for_asset_class_handler.get_aggregated_returns_for_asset_class_async(query.asset_class)
            )
            normalized_price_for_asset_class = self.cum_daily_vol_norm_returns_service.get_cumulative_daily_vol_normalized_returns(
                aggregated_returns_for_asset_class
            )
            normalized_price_this_instrument = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns(
                query.symbol
            )
            return self.normalized_price_for_asset_class_service.get_cumulative_daily_vol_normalized_returns(
                normalized_price_for_asset_class, normalized_price_this_instrument
            )

        except Exception:
            self.logger.exception("Unexpected error occurred while fetching normalied prices for asset class")
            raise
