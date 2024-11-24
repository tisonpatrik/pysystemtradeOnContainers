import pandas as pd

from common.logging.logger import AppLogger
from forecast.api.handlers.combined_forecast_without_multiplier_handler import CombinedForecastWithoutMultiplierHandler


class RawCombineForecastHandler:
    def __init__(self, combined_forecast_without_multiplier_handler: CombinedForecastWithoutMultiplierHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.combined_forecast_without_multiplier_handler = combined_forecast_without_multiplier_handler

    async def get_raw_combined_forecast_before_mappin_async(self, symbol: str) -> pd.Series:
        raw_combined_forecast = await self.combined_forecast_without_multiplier_handler.get_combined_forecast_without_multiplier_async(
            symbol
        )
        raise NotImplementedError("This method should be implemented in a subclass")
