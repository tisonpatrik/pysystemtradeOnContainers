import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.api.handlers.neg_skew_all_instruments_handler import NegSkewAllInstrumentsHandler


class CurrentAverageNegSkewOverAllAssetsHandler:
    def __init__(
        self,
        negskew_all_instruments_handler: NegSkewAllInstrumentsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.negskew_all_instruments_handler = negskew_all_instruments_handler

    async def get_current_avg_negskew_for_all_assets_async(self, lookback: int) -> pd.Series:
        self.logger.info("Fetching current average factor values for all assets")
        all_factor_values = await self.negskew_all_instruments_handler.get_negskew_for_all_instruments_async(lookback=lookback)
        return all_factor_values.ffill().mean(axis=1)
