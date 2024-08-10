import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolHandler:
    def __init__(self, prices_repository: PricesRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.daily_returns_vol_service = DailyReturnsVolService()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info(f"Starting to get daily returns volatility for {symbol}.")
            daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            return daily_returns_vol
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e