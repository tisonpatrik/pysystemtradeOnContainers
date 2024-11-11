import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.carry_client import CarryClient
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.carry import CarryService


class RelativeCarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_client = carry_client
        self.attenuation_handler = attenuation_handler
        self.carry_service = CarryService()

    async def get_relative_carry_async(self, symbol: str, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating Relative carry rule for %s", symbol)
        smoothed_carry = await self.carry_client.get_smoothed_carry_async(symbol)
        median_carry_for_asset_class = await self.carry_client.get_median_carry_for_asset_class_async(symbol)
        relative_carry = self.carry_service.calculate_relative_carry(
            smoothed_carry=smoothed_carry, median_carry_for_asset_class=median_carry_for_asset_class
        )
        signal = relative_carry.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
