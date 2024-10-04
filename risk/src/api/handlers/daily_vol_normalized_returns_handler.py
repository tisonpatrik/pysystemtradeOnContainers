import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from risk.src.services.daily_vol_normalized_returns_service import DailyVolnormalizedReturnsService


class DailyvolNormalizedReturnsHandler:
    def __init__(self, prices_repository: PricesRepository, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client
        self.daily_vol_normalized_returns_service = DailyVolnormalizedReturnsService()

    async def get_daily_vol_normalized_returns_async(self, instrument_code: str) -> pd.Series:
        self.logger.info("Fetching Daily volatility normalized returns for %s", instrument_code)
        try:
            returnvol_data = await self.raw_data_client.get_daily_returns_vol_async(instrument_code)
            prices = await self.prices_repository.get_daily_prices_async(instrument_code)
            return self.daily_vol_normalized_returns_service.get_daily_vol_normalized_returns(prices, returnvol_data)
        except Exception:
            self.logger.exception("Unexpected error occurred while fetching Daily volatility normalized returns")
            raise
