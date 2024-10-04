import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from risk.src.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from risk.src.api.handlers.daily_vol_normalized_price_for_asset_handler import DailyVolNormalizedPriceForAssetHandler


class NormalizedPricesForAssetClassHandler:
    def __init__(
        self,
        daily_vol_normalized_price_for_asset_handler: DailyVolNormalizedPriceForAssetHandler,
        cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalized_price_for_asset_handler = daily_vol_normalized_price_for_asset_handler
        self.cumulative_daily_vol_norm_returns_handler = cumulative_daily_vol_norm_returns_handler

    async def get_normalized_price_for_asset_class_async(self, query: GetNormalizedPriceForAssetClassQuery) -> pd.Series:
        try:
            self.logger.info("Fetching normalized prices for asset class %s", query)

            normalized_price_for_asset_class = (
                await self.daily_vol_normalized_price_for_asset_handler.daily_vol_normalized_price_for_asset_async(query.asset_class)
            )
            normalized_price_this_instrument = (
                await self.cumulative_daily_vol_norm_returns_handler.get_cumulative_daily_vol_normalized_returns_async(query.symbol)
            )
            return normalized_price_for_asset_class.reindex(normalized_price_this_instrument.index).ffill()

        except Exception:
            self.logger.exception("Unexpected error occurred while fetching normalied prices for asset class")
            raise
