import pandas as pd
from fastapi import HTTPException

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_dataframe, to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.daily_returns_vol import DailyReturnsVol
from common.src.validation.trading_signal import TradingSignal
from rules.src.services.accel import AccelService


class AccelHandler:
    def __init__(self, repository: Repository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_service = AccelService()
        self.repository = repository
        self.client = client

    async def get_accel_async(self, request: GetRuleForInstrumentQuery) -> pd.DataFrame:
        self.logger.info(f"Calculating Accel rule for {request}")
        daily_prices = await self._get_daily_prices_async(request.symbol)
        vol = await self._get_daily_retuns_vol_async(request.symbol)
        accel = self.accel_service.calculate_accel(daily_prices, vol, request.speed)
        return to_dataframe(accel, TradingSignal, str(TradingSignal.date_time), str(TradingSignal.value))

    async def _get_daily_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDailyPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = to_series(prices_data, DailyPrices, str(DailyPrices.date_time), str(DailyPrices.price))
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching currency for symbol {symbol}: {e}")
            raise

    async def _get_daily_retuns_vol_async(self, instrument_code: str) -> pd.Series:
        query = GetDailyReturnsVolQuery(symbol=instrument_code)
        try:
            vol_data = await self.client.get_data_async(query)
            vol = to_series(vol_data, DailyReturnsVol, str(DailyReturnsVol.date_time), str(DailyReturnsVol.vol))
            return vol
        except Exception as e:
            self.logger.error(f"Error fetching daily returns vol rate for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching daily returns vol rate")
