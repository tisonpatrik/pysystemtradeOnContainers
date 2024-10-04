import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.accel import AccelService


class AccelHandler:
    def __init__(self, prices_repository: PricesClient, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_service = AccelService()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client

    async def get_accel_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating Accel rule for %s by speed %d", symbol, speed)
            daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
            vol = await self.raw_data_client.get_daily_returns_vol_async(symbol)
            return self.accel_service.calculate_accel(daily_prices, vol, speed)
        except Exception:
            self.logger.exception("Error calculating accel rule for %s by speed %d", symbol, speed)
            raise
