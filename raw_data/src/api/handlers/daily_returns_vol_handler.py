import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from raw_data.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolHandler:
    def __init__(self, prices_repository: PricesRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.daily_returns_vol_service = DailyReturnsVolService()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Starting to get daily returns volatility for %s.", symbol)
            daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
            return self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
        except Exception:
            self.logger.exception("Error in processing instrument volatility")
            raise
