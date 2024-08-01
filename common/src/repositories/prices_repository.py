import pandas as pd

from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import list_to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices


class PricesRepository:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDailyPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = list_to_series(prices_data, DailyPrices, str(DailyPrices.date_time), str(DailyPrices.price))
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching currency for symbol {symbol}: {e}")
            raise

    async def get_denom_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDenomPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = list_to_series(prices_data, DenomPrices, DenomPrices.date_time, DenomPrices.price)  # type: ignore[arg-type]
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching denom price for symbol {symbol}: {e}")
            raise
