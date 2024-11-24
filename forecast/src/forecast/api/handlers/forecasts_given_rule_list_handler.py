import pandas as pd

from common.clients.rules_signals_client import RulesSignalsClient
from common.logging.logger import AppLogger
from common.validation.rule import Rule


class ForecastGivenRuleListHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.rules_signals_client = rules_signals_client

    async def get_forecasts_given_rule_list_async(self, instrument_code: str, rule_variation_list: list[Rule]) -> pd.DataFrame:
        forecasts = []
        rule_variation_names = []
        for rule_variation in rule_variation_list:
            forecast = await self.rules_signals_client.get_forecast_by_rule_async(instrument_code, rule_variation)
            forecasts.append(forecast)
            rule_variation_names.append(rule_variation.rule_variation_name)

        contacted = pd.concat(forecasts, axis=1)
        contacted.columns = pd.Index(rule_variation_names)
        return contacted.ffill()
