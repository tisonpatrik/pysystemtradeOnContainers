import numpy as np
import pandas as pd

from common.src.clients.carry_client import CarryClient
from common.src.cqrs.api_queries.rule_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.carry import CarryService


class RelativeCarryHandler:
    def __init__(self, carry_client: CarryClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_client = carry_client
        self.attenuation_handler = attenuation_handler
        self.carry_service = CarryService()

    async def get_relative_carry_async(self, query: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info("Calculating Relative carry rule for %s", query.symbol)
        smoothed_carry = await self.carry_client.get_smoothed_carry_async(query.symbol)
        median_carry_for_asset_class = await self.carry_client.get_median_carry_for_asset_class_async(query.symbol)
        relative_carry = self.carry_service.calculate_relative_carry(
            smoothed_carry=smoothed_carry, median_carry_for_asset_class=median_carry_for_asset_class
        )
        signal = relative_carry.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return signal
