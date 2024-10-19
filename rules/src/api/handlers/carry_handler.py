import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.carry_client import CarryClient
from rules.src.services.carry import CarryService


class CarryHandler:
    def __init__(self, carry_client: CarryClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_client = carry_client
        self.carry_service = CarryService()

    async def get_carry_async(self, symbol: str, smooth_days: int) -> pd.Series:
        try:
            self.logger.info("Calculating Carry rule for %s", symbol)
            raw_carry = await self.carry_client.get_raw_carry_async(symbol)
            return self.carry_service.calculate_raw_carry(raw_carry=raw_carry, smooth_days=smooth_days)

        except Exception:
            self.logger.exception("Error calculating Carry rule for %s", symbol)
            raise
