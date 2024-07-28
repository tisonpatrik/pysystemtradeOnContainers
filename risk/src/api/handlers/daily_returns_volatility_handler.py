import pandas as pd

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from common.src.utils.convertors import to_dataframe
from common.src.validation.daily_returns_vol import DailyReturnsVol
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolHandler:
    def __init__(self, prices_repository: PricesRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.prices_repository = prices_repository

    async def get_daily_returns_vol_async(self, position_query: GetDailyReturnsVolQuery) -> pd.DataFrame:
        try:
            self.logger.info(f"Starting to get daily returns volatility for {position_query}.")
            daily_prices = await self.prices_repository.get_daily_prices_async(position_query.symbol)
            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            return to_dataframe(daily_returns_vol, DailyReturnsVol, str(DailyReturnsVol.date_time), str(DailyReturnsVol.vol))
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e
