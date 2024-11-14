import pandas as pd

from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.logging.logger import AppLogger
from forecast.api.handlers.forecasts_given_rule_list_handler import ForecastGivenRuleListHandler


class WeightedForecastsWithoutMultiplierHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient, forecasts_given_rule_list_handler: ForecastGivenRuleListHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.rules_signals_client = rules_signals_client
        self.forecasts_given_rule_list_handler = forecasts_given_rule_list_handler

    async def get_weighted_forecasts_without_multiplier_async(self, symbol: str) -> pd.DataFrame:
        rule_variation_list = await self.rules_signals_client.get_trading_rule_list_async(symbol)
        forecasts = await self.forecasts_given_rule_list_handler.get_forecasts_given_rule_list_async(symbol, rule_variation_list)

        smoothed_daily_forecast_weights = await self.rules_signals_client.get_forecast_weights_async(symbol)
        smoothed_forecast_weights = smoothed_daily_forecast_weights.reindex(forecasts.index, method="ffill")

        return smoothed_forecast_weights * forecasts
