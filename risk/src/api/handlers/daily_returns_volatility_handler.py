import pandas as pd

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_dataframe, to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.daily_returns_vol import DailyReturnsVol
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolHandler:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.repository = repository

    async def get_daily_returns_vol_async(self, position_query: GetDailyReturnsVolQuery) -> pd.DataFrame:
        try:
            self.logger.info(f"Starting to get daily returns volatility for {position_query}.")
            daily_prices = await self._get_daily_prices_async(position_query.symbol)
            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            return to_dataframe(daily_returns_vol, DailyReturnsVol, str(DailyReturnsVol.date_time), str(DailyReturnsVol.vol))
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e

    async def _get_daily_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDailyPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = to_series(prices_data, DailyPrices, str(DailyPrices.date_time), str(DailyPrices.price))
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching currency for symbol {symbol}: {e}")
            raise
