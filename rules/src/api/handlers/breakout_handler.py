import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from rules.src.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, prices_repository: PricesRepository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.breakout_service = BreakoutService()
        self.prices_repository = prices_repository
        self.client = client

    async def get_breakout_async(self, request: GetRuleForInstrumentQuery) -> pd.Series:
        try:
            self.logger.info(f"Calculating Breakout rule for {request}")
            daily_prices = await self.prices_repository.get_daily_prices_async(request.symbol)
            breakout = self.breakout_service.calculate_breakout(daily_prices, request.speed)
            breakout = breakout.dropna()
            return breakout
        except Exception as e:
            self.logger.error(f"Error calculating breakout rule for {request}: {str(e)}")
            raise e
