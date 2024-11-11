import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.skew import SkewRuleService


class SkewAbsHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.skewabs_service = SkewRuleService()

    async def get_skewabs_async(self, symbol: str, speed: int, lookback: int, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating SkewAbs rule for %s", symbol)
        absolute_skew_deviation = await self.raw_data_client.absolute_skew_deviation_async(symbol, lookback)
        skewabs = self.skewabs_service.calculate_skew(demean_factor_value=absolute_skew_deviation, smooth=speed)
        signal = skewabs.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
