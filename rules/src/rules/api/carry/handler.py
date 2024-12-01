import numpy as np
import pandas as pd
from common.clients.old_carry_client import CarryClient
from common.logging.logger import AppLogger

from rules.api.carry.request import CarryQuery
from rules.services.carry import CarryService
from rules.services.normalization_service import NormalizationService
from rules.shared.attenutation_handler import AttenutationHandler


class CarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.carry_client = carry_client
        self.carry_service = CarryService()
        self.normalization_service = NormalizationService()

    async def get_carry_async(self, query: CarryQuery) -> pd.Series:
        self.logger.info('Calculating Carry rule for %s', query.symbol)
        raw_carry = await self.carry_client.get_raw_carry_async(query.symbol)
        carry = self.carry_service.calculate_carry(raw_carry=raw_carry, smooth_days=query.smooth_days)
        signal = carry.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
