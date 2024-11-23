import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_bdays_inyear
from raw_data.handlers.current_average_negskew_over_all_assets_handler import CurrentAverageNegSkewOverAllAssetsHandler


class HistoricAverageNegSkewAllAssetsHandler:
    def __init__(
        self,
        current_average_negskew_over_all_assets_handler: CurrentAverageNegSkewOverAllAssetsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.current_average_negskew_over_all_assets_handler = current_average_negskew_over_all_assets_handler

    async def get_historic_avg_factor_value_for_all_assets_async(self, lookback: int) -> pd.Series:
        self.logger.info("Fetching historic average factor values for all assets")
        span_years = 15
        cs_average_all_factors = await self.current_average_negskew_over_all_assets_handler.get_current_avg_negskew_for_all_assets_async(
            lookback=lookback
        )
        return cs_average_all_factors.ewm(get_bdays_inyear() * span_years).mean()
