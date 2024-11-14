import pandas as pd

from common.src.logging.logger import AppLogger
from forecast.api.handlers.raw_fixed_forecast_weights_handlers import RawFixedForecastWeightsHandler
from forecast.constants import USE_ESTIMATED_WEIGHTS


class RawMonthlyForecastWeightsHandler:
    def __init__(self, raw_fixed_forecast_weights_handlers: RawFixedForecastWeightsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_fixed_forecast_weights_handlers = raw_fixed_forecast_weights_handlers

    async def get_raw_monthly_forecast_weights_async(self, instrument_code: str) -> pd.DataFrame:
        # get estimated weights, will probably come back as annual data frame
        if USE_ESTIMATED_WEIGHTS:
            raise NotImplementedError("Estimated weights not implemented")
        ## will come back as 2*N data frame
        forecast_weights = await self.raw_fixed_forecast_weights_handlers.get_raw_fixed_forecast_weights_async(instrument_code)
        return pd.DataFrame()
        # ## FIXME NEED THIS TO APPLY TO GROUPINGS
        # return self._remove_expensive_rules_from_weights(instrument_code, forecast_weights)
