import numpy as np
import pandas as pd
from common.clients.old_carry_client import CarryClient
from common.logging.logger import AppLogger

from rules.api.relative_carry.request import RelativeCarryQuery
from rules.services.carry import CarryService
from rules.services.normalization_service import NormalizationService
from rules.shared.attenutation_handler import AttenutationHandler


class RelativeCarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_client = carry_client
        self.attenuation_handler = attenuation_handler
        self.normalization_service = NormalizationService()
        self.carry_service = CarryService()

    async def get_relative_carry_async(self, query: RelativeCarryQuery) -> pd.Series:
        self.logger.info('Calculating Relative carry rule for %s', query.symbol)
        smoothed_carry = await self.carry_client.get_smoothed_carry_async(query.symbol)
        median_carry_for_asset_class = await self.carry_client.get_median_carry_for_asset_class_async(query.symbol)
        relative_carry = self.carry_service.calculate_relative_carry(
            smoothed_carry=smoothed_carry, median_carry_for_asset_class=median_carry_for_asset_class
        )
        signal = relative_carry.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
