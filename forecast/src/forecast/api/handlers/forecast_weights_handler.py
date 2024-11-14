import pandas as pd

from common.src.logging.logger import AppLogger
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
        return pd.DataFrame()
        # # smooth out weights
        # forecast_smoothing_ewma_span = self.config.forecast_weight_ewma_span
        # smoothed_daily_forecast_weights = daily_forecast_weights_fixed_to_forecasts_unsmoothed.ewm(span=forecast_smoothing_ewma_span).mean()

        # # change rows so weights add to one (except for special case where all zeros)
        # return weights_sum_to_one(smoothed_daily_forecast_weights)
