from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from rules.src.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, repository: Repository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()
        self.repository = repository
        self.client = client

    async def get_assettrend_async(self, request: GetRuleForInstrumentQuery):
        self.logger.info(f"Calculating Breakout rule for {request}")
        # daily_prices = await self._get_daily_prices_async(request.symbol)
        # assettrend = self.assettrend_service.calculate_assettrend(daily_prices, request.speed)
        # return to_dataframe(assettrend, TradingSignal, str(TradingSignal.date_time), str(TradingSignal.value))
