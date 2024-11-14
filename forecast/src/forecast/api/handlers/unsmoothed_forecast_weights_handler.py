import pandas as pd

from common.src.logging.logger import AppLogger
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
        return pd.DataFrame()
        # # fix to forecast time series
        # forecast_weights_fixed_to_forecasts = self._fix_weights_to_forecasts(
        #     instrument_code=instrument_code,
        #     monthly_forecast_weights=monthly_forecast_weights,
        # )

        # # Remap to business day frequency so the smoothing makes sense also space saver
        # daily_forecast_weights_fixed_to_forecasts_unsmoothed = forecast_weights_fixed_to_forecasts.resample("1B").mean()

        # return daily_forecast_weights_fixed_to_forecasts_unsmoothed
