import numpy as np
import pandas as pd
from common.clients.old_carry_client import CarryClient
from common.logging.logger import AppLogger

from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.carry import CarryService
from rules.services.normalization_service import NormalizationService


class CarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.carry_client = carry_client
        self.carry_service = CarryService()
        self.normalization_service = NormalizationService()

    async def get_carry_async(
        self, symbol: str, smooth_days: int, use_attenuation: bool, scaling_factor: float, scaling_type: str
    ) -> pd.Series:
        self.logger.info('Calculating Carry rule for %s', symbol)
        raw_carry = await self.carry_client.get_raw_carry_async(symbol)
        carry = self.carry_service.calculate_carry(raw_carry=raw_carry, smooth_days=smooth_days)
        signal = carry.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=scaling_factor, raw_forecast=signal, scaling_type=scaling_type
        )
