import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_client import PricesClient
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, prices_repository: PricesClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.attenuation_handler = attenuation_handler
        self.breakout_service = BreakoutService()

    async def get_breakout_async(self, symbol: str, speed: int, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating Breakout rule for %s by speed %d", symbol, speed)
        daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
        breakout = self.breakout_service.calculate_breakout(daily_prices, speed)
        breakout = breakout.replace(0, np.nan)
        signal = breakout.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
