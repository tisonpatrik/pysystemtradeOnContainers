from common.clients.rules_signals_client import RulesSignalsClient
from common.logging.logger import AppLogger
from forecast.api.handlers.cheap_trading_rules_handler import CheapTradingRulesHandler


class ExpensiveTradingRulesPostProcessingHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient, cheap_trading_rules_handler: CheapTradingRulesHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.rules_signals_client = rules_signals_client
        self.cheap_trading_rules_handler = cheap_trading_rules_handler

    async def expensive_trading_rules_post_processing_async(self, instrument_code: str) -> list:
        rules = await self.rules_signals_client.get_trading_rule_list_async()
        cheap_rule_names = await self.cheap_trading_rules_handler.cheap_trading_rules_post_processing_async(instrument_code)
        return self.list_difference(rules, cheap_rule_names)

    def list_difference(self, list1: list, list2: list) -> list:
        raise NotImplementedError("This method should be implemented in a subclass")
