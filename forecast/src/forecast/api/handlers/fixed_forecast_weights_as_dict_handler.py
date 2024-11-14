from common.src.logging.logger import AppLogger
from forecast.api.handlers.expensive_trading_rules_post_processing_handler import ExpensiveTradingRulesPostProcessingHandler


class FixedForecastWeightsAsDictHandler:
    def __init__(self, expensive_trading_rules_post_processing_handler: ExpensiveTradingRulesPostProcessingHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.expensive_trading_rules_post_processing_handler = expensive_trading_rules_post_processing_handler

    async def get_fixed_forecast_weights_async(self, instrument_code: str) -> dict:
        expensive_trading_rules_post_processing = (
            await self.expensive_trading_rules_post_processing_handler.expensive_trading_rules_post_processing_async(instrument_code)
        )
        raise NotImplementedError("This method should be implemented in a subclass")
