import numpy as np
import pandas as pd

from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.momentum_handler import MomentumHandler


class MomentumRuleHandler:
    def __init__(self, momentum_handler: MomentumHandler, attenuation_handler: AttenutationHandler):
        self.momentum_handler = momentum_handler
        self.attenuation_handler = attenuation_handler

    async def get_momentum_async(self, symbol: str, speed: int, use_attenuation: bool) -> pd.Series:
        ewmac = await self.momentum_handler.get_momentum_signal_async(symbol, speed)
        signal = ewmac.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
