import pandas as pd

from common.logging.logger import AppLogger
from forecast.api.handlers.unsmoothed_forecast_weights_handler import UnsmoothedForecastWeightsHandler


class ForecastWeightsHandler:
    def __init__(self, unsmoothed_forecast_weights_handler: UnsmoothedForecastWeightsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.unsmoothed_forecast_weights_handler = unsmoothed_forecast_weights_handler

    async def get_forecast_weights_async(self, instrument_code: str) -> pd.DataFrame:
        # These will be in daily frequency
        daily_forecast_weights_fixed_to_forecasts_unsmoothed = (
            await self.unsmoothed_forecast_weights_handler.get_unsmoothed_forecast_weights_async(instrument_code)
        )
        raise NotImplementedError("This method should be implemented in a subclass")
