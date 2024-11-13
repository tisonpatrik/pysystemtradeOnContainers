import pandas as pd

from common.src.logging.logger import AppLogger


class WeightedForecastsWithoutMultiplierHandler:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    async def get_weighted_forecasts_without_multiplier_async(self, symbol: str) -> pd.Series:
        return pd.Series()
