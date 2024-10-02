import pandas as pd

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(
        self,
        prices_repository: PricesRepository,
        instruments_repository: InstrumentsRepository,
        raw_data_client: RawDataClient,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.prices_repository = prices_repository
        self.instruments_repository = instruments_repository
        self.instrument_vol_service = InstrumentCurrencyVolService()

    async def get_instrument_vol_for_symbol_async(self, query: GetInstrumentCurrencyVolQuery) -> pd.Series:
        try:
            denom_prices = await self.prices_repository.get_denom_prices_async(query.symbol)
            point_size = await self.instruments_repository.get_point_size_async(query.symbol)

            daily_returns_vol = await self.raw_data_client.get_daily_returns_vol_async(query.symbol)
            return self.instrument_vol_service.calculate_instrument_vol_async(denom_prices, daily_returns_vol, point_size.pointsize)
        except Exception:
            self.logger.exception("Error in processing instrument volatility")
            raise
