import pandas as pd

from common.logging.logger import AppLogger
from forecast.api.handlers.weighted_forecasts_without_multiplier_handler import WeightedForecastsWithoutMultiplierHandler


class CombinedForecastWithoutMultiplierHandler:
    def __init__(self, weighted_forecasts_without_multiplier_handler: WeightedForecastsWithoutMultiplierHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.weighted_forecasts_without_multiplier_handler = weighted_forecasts_without_multiplier_handler

    async def get_combined_forecast_without_multiplier_async(self, symbol: str) -> pd.Series:
        weighted_forecasts = await self.weighted_forecasts_without_multiplier_handler.get_weighted_forecasts_without_multiplier_async(
            symbol
        )
        return weighted_forecasts.sum(axis=1)
