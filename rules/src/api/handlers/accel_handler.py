import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.risk_client import RiskClient
from rules.src.services.accel import AccelService


class AccelHandler:
    def __init__(self, prices_repository: PricesRepository, risk_client: RiskClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_service = AccelService()
        self.prices_repository = prices_repository
        self.risk_client = risk_client

    async def get_accel_async(self, request: GetRuleForInstrumentQuery) -> pd.Series:
        try:
            self.logger.info(f"Calculating Accel rule for {request}")
            daily_prices = await self.prices_repository.get_daily_prices_async(request.symbol)
            vol = await self.risk_client.get_daily_retuns_vol_async(request.symbol)
            accel = self.accel_service.calculate_accel(daily_prices, vol, request.speed)
            accel = accel.dropna()
            return accel
        except Exception as e:
            self.logger.error(f"Error calculating accel rule for {request}: {str(e)}")
            raise e
