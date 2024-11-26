import numpy as np
import pandas as pd
from common.clients.raw_data_client import RawDataClient
from common.logging.logger import AppLogger

from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.ewmac_calc_vol_service import EwmacCalsVolService


class AssertTrendHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = EwmacCalsVolService()

    async def get_asserttrend_async(
        self, symbol: str, lfast: int, lslow: int, use_attenuation: bool, scaling_factor: float, scaling_type: str
    ) -> pd.Series:
        self.logger.info('Calculating AssetTrend rule for %s by speed %d', symbol, lslow)
        prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
        assettrend = self.assettrend_service.calculate_ewmac_calc_vol(prices, lfast, lslow)
        assettrend = assettrend.replace(0, np.nan)
        signal = assettrend.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
