import numpy as np
import pandas as pd
from common.logging.logger import AppLogger

from rules.api.accel.request import AccelQuery
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.momentum_handler import MomentumHandler
from rules.services.accel import AccelService
from rules.services.normalization_service import NormalizationService


class AccelHandler:
    def __init__(self, momentum_handler: MomentumHandler, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.attenuation_handler = attenuation_handler
        self.momentum_handler = momentum_handler
        self.accel_service = AccelService()
        self.normalization_service = NormalizationService()

    async def get_accel_async(self, query: AccelQuery) -> pd.Series:
        self.logger.info('Calculating Accel rule for %s by speed %d', query.symbol, query.lfast)
        lslow = query.lfast * 4
        ewmac = await self.momentum_handler.get_momentum_signal_async(query.symbol, query.lfast, lslow)
        accel = self.accel_service.calculate_accel(ewmac, query.lfast)
        signal = accel.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
