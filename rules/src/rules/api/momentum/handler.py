import numpy as np
import pandas as pd

from rules.api.momentum.request import MomentumQuery
from rules.services.normalization_service import NormalizationService
from rules.shared.attenutation_handler import AttenutationHandler
from rules.shared.momentum_handler import MomentumHandler


class MomentumRuleHandler:
    def __init__(self, momentum_handler: MomentumHandler, attenuation_handler: AttenutationHandler):
        self.momentum_handler = momentum_handler
        self.attenuation_handler = attenuation_handler
        self.normalization_service = NormalizationService()

    async def get_momentum_async(self, query: MomentumQuery) -> pd.Series:
        ewmac = await self.momentum_handler.get_momentum_signal_async(query.symbol, query.lfast, query.lslow)
        signal = ewmac.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
