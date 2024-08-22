import pandas as pd

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(
        self,
        prices_repository: PricesRepository,
        instruments_repository: InstrumentsRepository,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_vol_service = InstrumentCurrencyVolService()
        self.daily_returns_vol_service = DailyReturnsVolService()
        self.prices_repository = prices_repository
        self.instruments_repository = instruments_repository

    async def get_instrument_vol_for_symbol_async(self, position_query: GetInstrumentCurrencyVolQuery) -> pd.Series:
        try:
            denom_prices = await self.prices_repository.get_denom_prices_async(position_query.symbol)
            daily_prices = await self.prices_repository.get_daily_prices_async(position_query.symbol)
            point_size = await self.instruments_repository.get_point_size_async(position_query.symbol)
            print(denom_prices)

            daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(daily_prices)
            instrument_volatility = self.instrument_vol_service.calculate_instrument_vol_async(
                denom_prices, daily_returns_vol, point_size.pointsize
            )
            return instrument_volatility
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e
