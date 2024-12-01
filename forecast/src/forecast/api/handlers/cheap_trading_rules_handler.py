from common.clients.account_client import AccountClient
from common.clients.old_rules_signals_client import RulesSignalsClient
from common.logging.logger import AppLogger
from forecast.constants import CEILING_COST_SR


class CheapTradingRulesHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient, account_client: AccountClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.rules_signals_client = rules_signals_client
        self.account_client = account_client

    async def cheap_trading_rules_post_processing_async(self, instrument_code: str) -> list:
        ceiling_cost_SR = CEILING_COST_SR
        rules = await self.rules_signals_client.get_trading_rule_list_async()
        cheap_rule_list = []

        for rule_variation_name in rules:
            rule_cost = await self.account_client.get_SR_cost_for_instrument_forecast_async(instrument_code, rule_variation_name)
            if rule_cost <= ceiling_cost_SR:
                cheap_rule_list.append(rule_variation_name)

        return cheap_rule_list
