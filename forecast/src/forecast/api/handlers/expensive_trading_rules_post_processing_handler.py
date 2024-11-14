from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.logging.logger import AppLogger


class ExpensiveTradingRulesPostProcessingHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.rules_signals_client = rules_signals_client

    async def expensive_trading_rules_post_processing_async(self, instrument_code: str) -> list:
        rules = await self.rules_signals_client.get_trading_rule_list_async()
        return []
