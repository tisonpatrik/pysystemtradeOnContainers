import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from rules.src.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, prices_repository: PricesRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.breakout_service = BreakoutService()

    async def get_breakout_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info(f"Calculating Breakout rule for {symbol} by speed {speed}")
            daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
            breakout = self.breakout_service.calculate_breakout(daily_prices, speed)
            breakout = breakout.dropna()
            return breakout
        except Exception as e:
            self.logger.error(f"Error calculating breakout rule for {symbol} by speed {speed}: {str(e)}")
            raise e
