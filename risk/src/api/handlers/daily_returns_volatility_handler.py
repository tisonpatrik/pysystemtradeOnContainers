import pandas as pd

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_series
from common.src.validation.daily_prices import DailyPrices
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class DailyReturnsVolHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_vol_service = InstrumentCurrencyVolService()
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.repository = repository

    async def get_daily_returns_vol_async(self, position_query: GetDailyReturnsVolQuery) -> pd.Series:
        try:
            daily_prices = await self._get_daily_prices_async(position_query.symbol)
            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            return daily_returns_vol
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
