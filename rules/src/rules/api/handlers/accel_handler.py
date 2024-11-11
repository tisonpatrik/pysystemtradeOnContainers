import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.momentum_handler import MomentumHandler
from rules.services.accel import AccelService


class AccelHandler:
    def __init__(self, momentum_handler: MomentumHandler, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.accel_service = AccelService()

        self.momentum_handler = momentum_handler

    async def get_accel_async(self, symbol: str, speed: int, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating Accel rule for %s by speed %d", symbol, speed)
        ewmac = await self.momentum_handler.get_momentum_signal_async(symbol, speed)
        accel = self.accel_service.calculate_accel(ewmac, speed)
        signal = accel.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
