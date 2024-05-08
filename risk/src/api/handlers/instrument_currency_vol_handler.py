import pandas as pd

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.models.api_models.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.queries.get_denom_prices import GetDenomPriceQuery
from common.src.queries.get_point_size import GetPointSize
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
			denom_prices = await self._get_denom_prices(position_query.symbol)
			daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(denom_prices)
			point_size = await self._get_point_size(position_query.symbol)
			instrument_volatility = self.instrument_vol_service.calculate_instrument_vol_async(
				denom_prices, daily_returns_vol, point_size
			)
			return instrument_volatility
		except Exception as e:
			self.logger.error(f'Error in processing instrument volatility: {str(e)}')
			raise e

	async def _get_denom_prices(self, symbol: str) -> pd.Series:
		statement = GetDenomPriceQuery(symbol=symbol)
		try:
			prices = await self.repository.fetch_many_async(statement)
			if not prices:
				error_msg = f'No currency found for symbol: {symbol}'
				self.logger.error(error_msg)
				raise ValueError(error_msg)
			price_df = pd.DataFrame(prices)
			return pd.Series(data=price_df['price'].values, index=pd.to_datetime(price_df['date_time']))
		except Exception as e:
			self.logger.error(f'Database error when fetching currency for symbol {symbol}: {e}')
			raise

	async def _get_point_size(self, symbol: str) -> float:
		statement = GetPointSize(symbol=symbol)
		try:
			point_size = await self.repository.fetch_item_async(statement)
			if not point_size:
				error_msg = f'No currency found for symbol: {symbol}'
				self.logger.error(error_msg)
				raise ValueError(error_msg)
			return point_size['pointsize']
		except Exception as e:
			self.logger.error(f'Database error when fetching currency for symbol {symbol}: {e}')
			raise
