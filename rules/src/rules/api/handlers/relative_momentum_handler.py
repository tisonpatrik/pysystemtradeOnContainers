import numpy as np
import pandas as pd

from common.src.clients.raw_data_client import RawDataClient
from common.src.cqrs.api_queries.rule_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.normalization_handler import NormalizationHandler
from rules.services.relative_momentum import RelativeMomentumService


class RelativeMomentumHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler, scaling_handler: NormalizationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.scaling_handler = scaling_handler
        self.relative_momentum_service = RelativeMomentumService()

    async def get_relative_momentum_async(self, query: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info("Calculating Relative Momentum rule for %s", query.symbol)
        cumulative_daily_vol_norm_returns = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(query.symbol)
        normalized_prices_for_asset_class = await self.raw_data_client.get_normalized_prices_for_asset_class_async(query.symbol)
        relative_momentum = self.relative_momentum_service.calculate_relative_momentum(
            cumulative_daily_vol_norm_returns, normalized_prices_for_asset_class, query.speed
        )
        signal = relative_momentum.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return await self.scaling_handler.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
