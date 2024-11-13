import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.prices_client import PricesClient
from common.src.cqrs.api_queries.get_fx_prices import GetFxPricesQuery
from common.src.logging.logger import AppLogger
from raw_data.constants import DEFAULT_CURRENCY
from raw_data.services.fx_price_service import FxService


class FxPricesHandler:
    def __init__(self, instruments_client: InstrumentsClient, prices_client: PricesClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_client = instruments_client
        self.prices_client = prices_client
        self.fx_prices_service = FxService()

    async def get_fx_prices_for_symbol_async(self, get_fx_rate_query: GetFxPricesQuery) -> pd.Series:
        self.logger.info("Fetching FX prices for symbol %s", get_fx_rate_query.symbol)
        instrument_currency = await self.instruments_client.get_instrument_currency_async(get_fx_rate_query.symbol)
        base_currency = get_fx_rate_query.base_currency

        if instrument_currency.currency == base_currency:
            fx_data = self.fx_prices_service.get_default_rate_series()
        elif base_currency == DEFAULT_CURRENCY:
            fx_data = await self.prices_client.get_fx_rates_async(instrument_currency.currency, DEFAULT_CURRENCY)
        elif instrument_currency.currency == DEFAULT_CURRENCY:
            fx_data = await self.get_fx_prices_for_inversion(instrument_currency.currency, base_currency)
        else:
            fx_data = await self.get_fx_cross(instrument_currency.currency, base_currency)
        return fx_data

    async def get_fx_prices_for_inversion(self, instrument_currency: str, base_currency: str) -> pd.Series:
        try:
            raw_fx_data = await self.prices_client.get_fx_rates_async(base_currency, instrument_currency)
            return self.fx_prices_service.calculate_inversion(raw_fx_data)
        except Exception:
            self.logger.exception("Failed to get FX prices for inversion for %s", instrument_currency)
            raise

    async def get_fx_cross(self, instrument_currency: str, base_currency: str) -> pd.Series:
        try:
            currency1_vs_default = await self.prices_client.get_fx_rates_async(instrument_currency, DEFAULT_CURRENCY)
            currency2_vs_default = await self.prices_client.get_fx_rates_async(base_currency, DEFAULT_CURRENCY)
            return self.fx_prices_service.calculate_fx_cross(currency1_vs_default, currency2_vs_default)
        except Exception:
            self.logger.exception("Failed to calculate FX cross rate between %s and %u", instrument_currency, base_currency)
            raise
