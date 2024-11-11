import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.raw_data_client = raw_data_client
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()

    async def get_assettrend_async(self, symbol: str, speed: int, use_atttention: bool) -> pd.Series:
        self.logger.info("Calculating AssetTrend rule for %s by speed %d", symbol, speed)
        prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
        assettrend = self.assettrend_service.calculate_assettrend(prices, speed)
        assettrend = assettrend.replace(0, np.nan)
        return assettrend
