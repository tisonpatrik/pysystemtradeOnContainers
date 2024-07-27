import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.cqrs.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_dataframe, to_series
from common.src.validation.daily_prices import DailyPrices
from common.src.validation.trading_signal import TradingSignal
from rules.src.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, repository: Repository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.breakout_service = BreakoutService()
        self.repository = repository
        self.client = client

    async def get_breakout_async(self, request: GetRuleForInstrumentQuery):
        self.logger.info(f"Calculating Breakout rule for {request}")
        daily_prices = await self._get_daily_prices_async(request.symbol)
        breakout = self.breakout_service.calculate_breakout(daily_prices, request.speed)
        return to_dataframe(breakout, TradingSignal, str(TradingSignal.date_time), str(TradingSignal.value))

    async def _get_daily_prices_async(self, symbol: str) -> pd.Series:
        statement = GetDailyPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = to_series(prices_data, DailyPrices, str(DailyPrices.date_time), str(DailyPrices.price))
            return prices
        except Exception as e:
            self.logger.error(f"Database error when fetching currency for symbol {symbol}: {e}")
            raise
