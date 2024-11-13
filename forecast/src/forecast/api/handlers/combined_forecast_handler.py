import pandas as pd

from common.src.logging.logger import AppLogger
from forecast.api.handlers.raw_combined_forecast_handler import RawCombineForecastHandler


class CombineForecastHandler:
    def __init__(self, raw_combined_forecast_handler: RawCombineForecastHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_combined_forecast_handler = raw_combined_forecast_handler

    async def get_combined_forecast_async(self, symbol: str) -> pd.Series:
        self.logger.info("Getting combined forecast for symbol %s", symbol)
        raw_multiplied_combined_forecast = await self.raw_combined_forecast_handler.get_raw_combined_forecast_before_mappin_async(symbol)
        return raw_multiplied_combined_forecast
