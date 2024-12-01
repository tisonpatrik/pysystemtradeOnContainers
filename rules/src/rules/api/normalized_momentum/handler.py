import numpy as np
import pandas as pd
from common.clients.old_raw_data_client import RawDataClient
from common.logging.logger import AppLogger

from rules.api.normalized_momentum.request import NormalizedMomentumQuery
from rules.services.ewmac_calc_vol_service import EwmacCalsVolService
from rules.shared.attenutation_handler import AttenutationHandler


class NormalizedMomentumHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.assettrend_service = EwmacCalsVolService()

    async def get_normalized_momentum_async(self, query: NormalizedMomentumQuery) -> pd.Series:
        self.logger.info('Calculating AssetTrend rule for %s by speed %d', query.symbol, query.lslow)
        prices = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(query.symbol)
        assettrend = self.assettrend_service.calculate_ewmac_calc_vol(prices, query.lfast, query.lslow)
        assettrend = assettrend.replace(0, np.nan)
        signal = assettrend.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return signal
