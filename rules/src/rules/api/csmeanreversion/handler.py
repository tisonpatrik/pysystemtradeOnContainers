import numpy as np
import pandas as pd
from common.clients.old_raw_data_client import RawDataClient
from common.logging.logger import AppLogger

from rules.api.csmeanreversion.request import CSMeanReversionQuery
from rules.services.cross_sectional_mean_reversion import CSMeanReversionService
from rules.services.normalization_service import NormalizationService
from rules.shared.attenutation_handler import AttenutationHandler


class CSMeanReversionHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.normalization_service = NormalizationService()
        self.cs_mean_reversion_service = CSMeanReversionService()

    async def get_cs_mean_reversion_async(self, query: CSMeanReversionQuery) -> pd.Series:
        self.logger.info('Calculating Cross sectional mean reversion rule for %s with speed %d', query.symbol, query.horizon)
        symbol_prices = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(query.symbol)
        asset_prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(query.symbol)
        cs_mean_reversion = self.cs_mean_reversion_service.calculate_cross_sectional_mean_reversion(
            normalized_price_this_instrument=symbol_prices, normalized_price_for_asset_class=asset_prices, horizon=query.horizon
        )
        signal = cs_mean_reversion.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(
                symbol=query.symbol, raw_signal=signal
            )
        return await self.normalization_service.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
