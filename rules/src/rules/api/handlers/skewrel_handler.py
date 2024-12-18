import numpy as np
import pandas as pd

from common.src.clients.raw_data_client import RawDataClient
from common.src.cqrs.api_queries.rule_queries.get_skewrel import GetSkewRelQuery
from common.src.logging.logger import AppLogger
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.normalization_handler import NormalizationHandler
from rules.services.skew import SkewRuleService


class SkewRelHandler:
    def __init__(self, raw_data_client: RawDataClient, attenuation_handler: AttenutationHandler, scaling_handler: NormalizationHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.attenuation_handler = attenuation_handler
        self.scaling_handler = scaling_handler
        self.skew_service = SkewRuleService()

    async def get_skewrel_async(self, query: GetSkewRelQuery) -> pd.Series:
        self.logger.info("Calculating SkewAbs rule for %s with smooth %d", query.symbol, query.smooth)
        relative_skew_deviation = await self.raw_data_client.relative_skew_deviation_async(query.symbol, query.lookback)
        skewrel = self.skew_service.calculate_skew(demean_factor_value=relative_skew_deviation, smooth=query.smooth)
        signal = skewrel.replace(0, np.nan)
        if query.use_attenuation:
            signal = await self.attenuation_handler.apply_attenutation_to_trading_signal_async(symbol=query.symbol, raw_signal=signal)
        return await self.scaling_handler.apply_normalization_signal_async(
            scaling_factor=query.scaling_factor, raw_forecast=signal, scaling_type=query.scaling_type
        )
