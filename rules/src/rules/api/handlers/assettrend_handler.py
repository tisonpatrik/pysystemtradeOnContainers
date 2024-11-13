import numpy as np
import pandas as pd

from common.src.clients.raw_data_client import RawDataClient
from common.src.cqrs.api_queries.rule_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()

    async def get_assettrend_async(self, query: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info("Calculating AssetTrend rule for %s by speed %d", query.symbol, query.speed)
        prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(query.symbol)
        assettrend = self.assettrend_service.calculate_assettrend(prices, query.speed)
        assettrend = assettrend.replace(0, np.nan)
        signal = assettrend.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return signal
