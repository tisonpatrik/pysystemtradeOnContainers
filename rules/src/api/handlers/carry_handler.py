import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.risk_client import RiskClient
from rules.src.services.carry import CarryService


class CarryHandler:
    def __init__(self, risk_client: RiskClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_client = risk_client
        self.carry_service = CarryService()

    async def get_carry_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Calculating Carry rule for %s", symbol)
            daily_returns_vol = await self.risk_client.get_daily_retuns_vol_async(symbol)
            return pd.Series()

        except Exception:
            self.logger.exception("Error calculating Carry rule for %s", symbol)
            raise
