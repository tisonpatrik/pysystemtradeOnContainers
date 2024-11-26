import numpy as np
import pandas as pd
from common.clients.prices_client import PricesClient
from common.logging.logger import AppLogger

from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.breakout import BreakoutService
from rules.services.normalization_service import NormalizationService


class BreakoutHandler:
    def __init__(self, prices_client: PricesClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_client = prices_client
        self.attenuation_handler = attenuation_handler
        self.breakout_service = BreakoutService()
        self.normalization_service = NormalizationService()

    async def get_breakout_async(
        self, symbol: str, lookback: int, use_attenuation: bool, scaling_factor: float, scaling_type: str
    ) -> pd.Series:
        self.logger.info('Calculating Breakout rule for %s by speed %d', symbol, lookback)
        daily_prices = await self.prices_client.get_daily_prices_async(symbol)
        breakout = self.breakout_service.calculate_breakout(daily_prices, lookback)
        breakout = breakout.replace(0, np.nan)
        signal = breakout.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=scaling_factor, raw_forecast=signal, scaling_type=scaling_type
        )
