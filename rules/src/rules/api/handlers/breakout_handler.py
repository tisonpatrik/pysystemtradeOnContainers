import numpy as np
import pandas as pd

from common.src.clients.prices_client import PricesClient
from common.src.cqrs.api_queries.rule_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, prices_client: PricesClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_client = prices_client
        self.attenuation_handler = attenuation_handler
        self.breakout_service = BreakoutService()

    async def get_breakout_async(self, query: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info("Calculating Breakout rule for %s by speed %d", query.symbol, query.speed)
        daily_prices = await self.prices_client.get_daily_prices_async(query.symbol)
        breakout = self.breakout_service.calculate_breakout(daily_prices, query.speed)
        breakout = breakout.replace(0, np.nan)
        signal = breakout.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return signal
