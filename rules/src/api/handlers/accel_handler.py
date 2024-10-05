import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.api.handlers.momentum_handler import MomentumHandler
from rules.src.services.accel import AccelService


class AccelHandler:
    def __init__(self, momentum_handler: MomentumHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_service = AccelService()

        self.momentum_handler = momentum_handler

    async def get_accel_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating Accel rule for %s by speed %d", symbol, speed)
            ewmac = await self.momentum_handler.get_momentum_async(symbol, speed)
            return self.accel_service.calculate_accel(ewmac, speed)
        except Exception:
            self.logger.exception("Error calculating accel rule for %s by speed %d", symbol, speed)
            raise
