import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.services.cross_sectional_mean_reversion import CSMeanReversionService


class CSMeanReversionHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.cs_mean_reversion_service = CSMeanReversionService()

    async def get_cs_mean_reversion_async(self, symbol: str, speed: int, use_attenuation: bool) -> pd.Series:
        self.logger.info("Calculating Cross sectional mean reversion rule for %s with speed %d", symbol, speed)
        symbol_prices = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(symbol)
        asset_prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
        cs_mean_reversion = self.cs_mean_reversion_service.calculate_cross_sectional_mean_reversion(
            normalized_price_this_instrument=symbol_prices, normalized_price_for_asset_class=asset_prices, horizon=speed
        )
        signal = cs_mean_reversion.replace(0, np.nan)
        if use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=symbol, raw_signal=signal)
        return signal
