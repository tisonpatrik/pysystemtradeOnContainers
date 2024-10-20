import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.raw_data_client = raw_data_client
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()

    async def get_assettrend_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating AssetTrend rule for %s by speed %d", symbol, speed)
            prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
            return self.assettrend_service.calculate_assettrend(prices, speed)
        except Exception:
            self.logger.exception("Error calculating AssetTrend rule for %s by speed %d", symbol, speed)
            raise
