import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.raw_carry_handler import RawCarryHandler
from raw_data.src.services.smooth_carry_service import SmoothCarryService


class SmoothCarryHandler:
    def __init__(self, raw_carry_handler: RawCarryHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_carry_handler = raw_carry_handler
        self.smooth_carry_service = SmoothCarryService()

    async def get_smooth_carry_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Fetching Smooth Carry for symbol %s", symbol)
            carry = await self.raw_carry_handler.get_raw_carry_async(symbol)
            return self.smooth_carry_service.calculate_smooth_carry(carry)
        except Exception:
            self.logger.exception("Unexpected error occurred while geting Smooth Carry")
            raise
