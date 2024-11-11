import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.services.skew import SkewRuleService


class SkewRelHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.skew_service = SkewRuleService()

    async def get_skewrel_async(self, symbol: str, speed: int, lookback: int, use_atttention: bool) -> pd.Series:
        self.logger.info("Calculating SkewAbs rule for %s", symbol)
        relative_skew_deviation = await self.raw_data_client.relative_skew_deviation_async(symbol, lookback)
        skewrel = self.skew_service.calculate_skew(demean_factor_value=relative_skew_deviation, smooth=speed)
        skewrel = skewrel.replace(0, np.nan)
        return skewrel
