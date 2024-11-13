import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.cqrs.api_queries.get_normalized_price_for_asset_class import GetNormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from raw_data.api.handlers.daily_vol_normalized_price_for_asset_handler import DailyVolNormalizedPriceForAssetHandler


class NormalizedPricesForAssetClassHandler:
    def __init__(
        self,
        instruments_client: InstrumentsClient,
        daily_vol_normalized_price_for_asset_handler: DailyVolNormalizedPriceForAssetHandler,
        cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instruments_client
        self.daily_vol_normalized_price_for_asset_handler = daily_vol_normalized_price_for_asset_handler
        self.cumulative_daily_vol_norm_returns_handler = cumulative_daily_vol_norm_returns_handler

    async def get_normalized_price_for_asset_class_async(self, query: GetNormalizedPriceForAssetClassQuery) -> pd.Series:
        self.logger.info("Fetching normalized prices for asset class %s", query)
        asset_class = await self.instrument_repository.get_asset_class_async(query.symbol)

        normalized_price_for_asset_class = (
            await self.daily_vol_normalized_price_for_asset_handler.daily_vol_normalized_price_for_asset_async(asset_class)
        )
        normalized_price_this_instrument = (
            await self.cumulative_daily_vol_norm_returns_handler.get_cumulative_daily_vol_normalized_returns_async(query.symbol)
        )
        return normalized_price_for_asset_class.reindex(normalized_price_this_instrument.index).ffill()
