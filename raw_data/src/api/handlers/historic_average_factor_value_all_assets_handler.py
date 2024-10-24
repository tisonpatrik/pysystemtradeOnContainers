import pandas as pd

from common.src.cqrs.api_queries.get_historic_average_factor_value_all_assets import GetHistoricAverageFactorValueAllAssetsQuery
from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_bdays_inyear
from raw_data.src.api.handlers.current_average_factor_values_over_all_assets_handler import CurrentAverageFactorValuesOverAllAssetsHandler


class HistoricAverageFactorValueAllAssetsHandler:
    def __init__(
        self,
        current_average_factor_values_over_all_assets_handler: CurrentAverageFactorValuesOverAllAssetsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.current_average_factor_values_over_all_assets_handler = current_average_factor_values_over_all_assets_handler

    async def get_historic_avg_factor_value_for_all_assets_async(self, query: GetHistoricAverageFactorValueAllAssetsQuery) -> pd.Series:
        try:
            span_years = 15
            cs_average_all_factors = (
                await self.current_average_factor_values_over_all_assets_handler.get_current_avg_factor_values_for_all_assets_async(
                    factor_name=query.factor_name, lookback=query.lookback
                )
            )
            return cs_average_all_factors.ewm(get_bdays_inyear() * span_years).mean()
        except Exception:
            self.logger.exception("Error in processing historic average factor value for all assets")
            raise
