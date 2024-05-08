import pandas as pd

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.models.api_models.get_fx_rate import GetFxRateQuery
from common.src.queries.get_fx_prices import GetFxPrices
from common.src.queries.get_instrument_currency import GetInstrumentCurrency
from raw_data.src.services.fx_price_service import FxService
from raw_data.src.validation.fx_prices import FxPrices
from raw_data.src.validation.instrument_currency import InstrumentCurrency


class FxPricesHandler:
	def __init__(self, repository: Repository):
		self.logger = AppLogger.get_instance().get_logger()
		self.repository = repository
		self.default_currency = 'USD'
		self.fx_prices_service = FxService()

	async def get_fx_prices_for_symbol_async(self, get_fx_rate_query: GetFxRateQuery) -> pd.Series:
		try:
			instrument_currency = await self._get_instrument_currency(get_fx_rate_query.symbol)

			base_currency = get_fx_rate_query.base_currency

			if base_currency == instrument_currency.currency:
				fx_data = self.fx_prices_service.get_default_rate_series()
			elif instrument_currency.currency == 'USD':
				fx_data = await self.get_standard_fx_prices_async(instrument_currency.currency)
			elif base_currency == 'USD':
				fx_data = await self.get_fx_prices_for_inversion(instrument_currency.currency)
			else:
				fx_data = await self.get_fx_cross(instrument_currency.currency, base_currency)

			return fx_data.head()

		except ValueError:
			raise  # Re-raise handled errors for external handling
		except Exception as e:
			self.logger.error(f'Unexpected error occurred while fetching FX prices: {e}')
			raise RuntimeError(f'An unexpected error occurred: {e}')

	async def _get_instrument_currency(self, symbol: str) -> InstrumentCurrency:
		statement = GetInstrumentCurrency(symbol=symbol)
		try:
			currency = await self.repository.fetch_item_async(statement)
			currency = InstrumentCurrency(**currency)
			return currency
		except Exception as e:
			self.logger.error(f'Database error when fetching currency for symbol {symbol}: {e}')
			raise

	async def get_standard_fx_prices_async(self, instrument_currency: str) -> pd.Series:
		fx_code = f'{instrument_currency}{self.default_currency}'
		statement = GetFxPrices(fx_code=fx_code)
		try:
			fx_data = await self.repository.fetch_many_async(statement)
			fx_dataframe = pd.DataFrame(fx_data)
			fx_prices = FxPrices.validate(fx_dataframe)
			return fx_prices
		except Exception as e:
			self.logger.error(f'Failed to fetch FX prices for {fx_code}: {e}')
			raise

	async def get_fx_prices_for_inversion(self, instrument_currency: str) -> pd.Series:
		try:
			raw_fx_data = await self.get_standard_fx_prices_async(instrument_currency)
			inverted_fx_data = self.fx_prices_service.calculate_inversion(raw_fx_data)
			return inverted_fx_data
		except Exception as e:
			self.logger.error(f'Failed to get FX prices for inversion for {instrument_currency}: {e}')
			raise

	async def get_fx_cross(self, instrument_currency: str, base_currency: str) -> pd.Series:
		try:
			currency1_vs_default = await self.get_standard_fx_prices_async(instrument_currency)
			currency2_vs_default = await self.get_standard_fx_prices_async(base_currency)
			fx_rate_series = self.fx_prices_service.calculate_fx_cross(currency1_vs_default, currency2_vs_default)
			return fx_rate_series
		except Exception as e:
			self.logger.error(
				f'Failed to calculate FX cross rate between {instrument_currency} and {base_currency}: {e}'
			)
			raise
