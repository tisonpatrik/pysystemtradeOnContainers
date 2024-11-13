import numpy as np
import pandas as pd

from common.src.cqrs.api_queries.rule_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.momentum_handler import MomentumHandler
from rules.api.handlers.normalization_handler import NormalizationHandler
from rules.services.accel import AccelService


class AccelHandler:
    def __init__(self, momentum_handler: MomentumHandler, attenuation_handler: AttenutationHandler, scaling_handler: NormalizationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.momentum_handler = momentum_handler
        self.scaling_handler = scaling_handler
        self.accel_service = AccelService()

    async def get_accel_async(self, query: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info("Calculating Accel rule for %s by speed %d", query.symbol, query.speed)
        ewmac = await self.momentum_handler.get_momentum_signal_async(query.symbol, query.speed)
        accel = self.accel_service.calculate_accel(ewmac, query.speed)
        signal = accel.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return await self.scaling_handler.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
