import numpy as np
import pandas as pd

from common.clients.raw_data_client import RawDataClient
from common.cqrs.api_queries.rule_queries.get_assettrend import GetAssetTrendQuery
from common.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.normalization_handler import NormalizationHandler
from rules.services.ewmac_calc_vol_service import EwmacCalsVolService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler, scaling_handler: NormalizationHandler):
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.logger = AppLogger.get_instance().get_logger()
        self.scaling_handler = scaling_handler
        self.assettrend_service = EwmacCalsVolService()

    async def get_assettrend_async(self, query: GetAssetTrendQuery) -> pd.Series:
        self.logger.info("Calculating AssetTrend rule for %s by speed %d", query.symbol, query.lslow)
        prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(query.symbol)
        assettrend = self.assettrend_service.calculate_ewmac_calc_vol(prices, query.lfast, query.lslow)
        assettrend = assettrend.replace(0, np.nan)
        signal = assettrend.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return signal
