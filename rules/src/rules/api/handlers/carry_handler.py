import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.carry_client import CarryClient
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.carry import CarryService


class CarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.carry_client = carry_client
        self.carry_service = CarryService()

    async def get_carry_async(self, symbol: str, smooth_days: int, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating Carry rule for %s", symbol)
        raw_carry = await self.carry_client.get_raw_carry_async(symbol)
        carry = self.carry_service.calculate_carry(raw_carry=raw_carry, smooth_days=smooth_days)
        signal = carry.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
