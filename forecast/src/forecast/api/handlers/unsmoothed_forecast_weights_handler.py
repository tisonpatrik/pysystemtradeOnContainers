import pandas as pd

from common.logging.logger import AppLogger
from forecast.api.handlers.raw_monthly_forecast_weights_handler import RawMonthlyForecastWeightsHandler


class UnsmoothedForecastWeightsHandler:
    def __init__(self, raw_monthly_forecast_weights_handler: RawMonthlyForecastWeightsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_monthly_forecast_weights_handler = raw_monthly_forecast_weights_handler

    async def get_unsmoothed_forecast_weights_async(self, instrument_code: str) -> pd.DataFrame:
        # note these might include missing weights, eg too expensive, or absent
        # from fixed weights
        # These are monthly to save space, or possibly even only 2 rows long
        monthly_forecast_weights = await self.raw_monthly_forecast_weights_handler.get_raw_monthly_forecast_weights_async(instrument_code)
        raise NotImplementedError("This method should be implemented in a subclass")
