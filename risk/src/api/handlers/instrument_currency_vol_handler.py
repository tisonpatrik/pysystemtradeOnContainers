import pandas as pd

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.cqrs.db_queries.get_denom_prices import GetDenomPriceQuery
from common.src.cqrs.db_queries.get_point_size import GetPointSize
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic, to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.denom_prices import DenomPrices
from common.src.validation.point_size import PointSize
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_vol_service = InstrumentCurrencyVolService()
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.repository = repository

    async def get_instrument_vol_for_symbol_async(self, position_query: GetInstrumentCurrencyVolQuery) -> pd.Series:
        try:
            denom_prices = await self._get_denom_prices_async(position_query.symbol)
            daily_prices = await self._get_daily_prices_async(position_query.symbol)
            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            point_size = await self._get_point_size_async(position_query.symbol)
            instrument_volatility = self.instrument_vol_service.calculate_instrument_vol_async(
                denom_prices, daily_returns_vol, point_size.point_size
            )
            return instrument_volatility
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

    async def _get_denom_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDenomPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = to_series(prices_data, DenomPrices, DenomPrices.date_time, DenomPrices.price)  # type: ignore[arg-type]
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching denom price for symbol {symbol}: {e}")
            raise

    async def _get_point_size_async(self, symbol: str) -> PointSize:
        statement = GetPointSize(symbol=symbol)
        try:
            point_size_data = await self.repository.fetch_item_async(statement)
            point_size = to_pydantic(point_size_data, PointSize)
            if point_size is None:
                raise ValueError(f"No data found for symbol {symbol}")
            return point_size
        except Exception as e:
            self.logger.error(f"Database error when fetching point size for symbol {symbol}: {e}")
            raise
