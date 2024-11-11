import numpy as np
import pandas as pd

from rules.api.handlers.momentum_handler import MomentumHandler


class MomentumRuleHandler:
    def __init__(self, momentum_handler: MomentumHandler):
        self.momentum_handler = momentum_handler

    async def get_momentum_async(self, symbol: str, speed: int, use_atttention: bool) -> pd.Series:
        ewmac = await self.momentum_handler.get_momentum_signal_async(symbol, speed)
        ewmac = ewmac.replace(0, np.nan)
        return ewmac
