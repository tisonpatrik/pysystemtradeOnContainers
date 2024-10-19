import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler


class DailyVolNormalizedPriceForAssetHandler:
    def __init__(self, aggregated_returns_for_asset_handler: AggregatedReturnsForAssetClassHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.aggregated_returns_for_asset_handler = aggregated_returns_for_asset_handler

    async def daily_vol_normalized_price_for_asset_async(self, asset: str) -> pd.Series:
        try:
            self.logger.info("Fetching daily volatility normalized prices for asset class %s", asset)
            aggregated_returns_for_asset_class = await self.aggregated_returns_for_asset_handler.get_aggregated_returns_for_asset_async(
                asset
            )
            return aggregated_returns_for_asset_class.cumsum()

        except Exception:
            self.logger.exception("Unexpected error occurred while fetching normalied prices for asset class")
            raise
