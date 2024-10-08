import pandas as pd

from common.src.cqrs.api_queries.get_fx_rate import GetFxRateQuery
from common.src.cqrs.db_queries.get_fx_prices import GetDailyFxPrices
from common.src.cqrs.db_queries.get_instrument_currency import GetInstrumentCurrency
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.fx_prices import FxPrices
from raw_data.src.services.fx_price_service import FxService
from raw_data.src.validation.instrument_currency import InstrumentCurrency


class FxPricesHandler:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.default_currency = "USD"
        self.fx_prices_service = FxService()

    async def get_fx_prices_for_symbol_async(self, get_fx_rate_query: GetFxRateQuery) -> pd.Series:
        try:
            self.logger.info("Fetching FX prices for symbol %s", get_fx_rate_query.symbol)
            instrument_currency = await self._get_instrument_currency(get_fx_rate_query.symbol)
            base_currency = get_fx_rate_query.base_currency

            if instrument_currency.currency == base_currency:
                fx_data = self.fx_prices_service.get_default_rate_series()
            elif base_currency == self.default_currency:
                fx_data = await self.get_standard_fx_prices_async(instrument_currency.currency, self.default_currency)
            elif instrument_currency.currency == self.default_currency:
                fx_data = await self.get_fx_prices_for_inversion(instrument_currency.currency, base_currency)
            else:
                fx_data = await self.get_fx_cross(instrument_currency.currency, base_currency)
            return fx_data

        except Exception:
            self.logger.exception("Unexpected error occurred while fetching FX prices")
            raise

    async def _get_instrument_currency(self, symbol: str) -> InstrumentCurrency:
        statement = GetInstrumentCurrency(symbol=symbol)
        try:
            currency_data = await self.repository.fetch_item_async(statement)
            currency = to_pydantic(currency_data, InstrumentCurrency)
            if currency is None:
                raise ValueError(f"No data found for symbol {symbol}")
            return currency
        except Exception:
            self.logger.exception("Database error when fetching currency for symbol %s", symbol)
            raise

    async def get_standard_fx_prices_async(self, instrument_currency: str, conversion_currency: str) -> pd.Series:
        fx_code = f"{instrument_currency}{conversion_currency}"
        statement = GetDailyFxPrices(fx_code=fx_code)
        try:
            fx_prices_data = await self.repository.fetch_many_async(statement)
            return FxPrices.from_db_to_series(fx_prices_data)
        except Exception:
            self.logger.exception("Failed to fetch FX prices for %s", fx_code)
            raise

    async def get_fx_prices_for_inversion(self, instrument_currency: str, base_currency: str) -> pd.Series:
        try:
            raw_fx_data = await self.get_standard_fx_prices_async(base_currency, instrument_currency)
            return self.fx_prices_service.calculate_inversion(raw_fx_data)
        except Exception:
            self.logger.exception("Failed to get FX prices for inversion for %s", instrument_currency)
            raise

    async def get_fx_cross(self, instrument_currency: str, base_currency: str) -> pd.Series:
        try:
            currency1_vs_default = await self.get_standard_fx_prices_async(instrument_currency, self.default_currency)
            currency2_vs_default = await self.get_standard_fx_prices_async(base_currency, self.default_currency)
            return self.fx_prices_service.calculate_fx_cross(currency1_vs_default, currency2_vs_default)
        except Exception:
            self.logger.exception("Failed to calculate FX cross rate between %s and %u", instrument_currency, base_currency)
            raise
