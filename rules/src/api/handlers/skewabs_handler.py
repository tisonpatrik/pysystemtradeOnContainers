import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.skewabs import SkewabsService


class SkewAbsHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.skewabs_service = SkewabsService()

    async def get_skewabs_async(self, symbol: str, speed: int, lookback: int) -> pd.Series:
        self.logger.info("Calculating Relative Momentum rule for %s", symbol)
        absolute_skew_deviation = await self.raw_data_client.absolute_skew_deviation_async(symbol, lookback)
        return self.skewabs_service.calculate_skewabs(demean_factor_value=absolute_skew_deviation, smooth=speed)
