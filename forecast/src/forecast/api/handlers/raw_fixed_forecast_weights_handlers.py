import pandas as pd

from common.logging.logger import AppLogger
from forecast.api.handlers.fixed_forecast_weights_as_dict_handler import FixedForecastWeightsAsDictHandler


class RawFixedForecastWeightsHandler:
    def __init__(self, fixed_forecast_weights_as_dict_handler: FixedForecastWeightsAsDictHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.fixed_forecast_weights_as_dict_handler = fixed_forecast_weights_as_dict_handler

    async def get_raw_fixed_forecast_weights_async(self, instrument_code: str) -> pd.DataFrame:
        # Now we have a dict, fixed_weights.
        # Need to turn into a timeseries covering the range of forecast
        # dates

        fixed_weights = await self.fixed_forecast_weights_as_dict_handler.get_fixed_forecast_weights_async(instrument_code)

        rule_variation_list = sorted(fixed_weights.keys())
        raise NotImplementedError("This method should be implemented in a subclass")
