import pandas as pd

from common.src.logging.logger import AppLogger
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
        return pd.DataFrame()

        # forecasts = self.get_all_forecasts(instrument_code, rule_variation_list)
        # forecasts_time_index = forecasts.index
        # forecast_columns_to_align = forecasts.columns

        # # Turn into a 2 row data frame aligned to forecast names
        # forecast_weights = from_dict_of_values_to_df(fixed_weights, forecasts_time_index, columns=forecast_columns_to_align)

        # ## Should be monthly for consistency, but span all data
        # return reindex_last_monthly_include_first_date(forecast_weights)
