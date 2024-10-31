import pandas as pd

from common.src.cqrs.api_queries.get_demanded_factor_value_query import GetDemandedFactorValueQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.historic_average_factor_value_all_assets_handler import HistoricAverageFactorValueAllAssetsHandler
from raw_data.src.api.handlers.skew_handler import SkewHandler


class DemandedFactorValueHandler:
    def __init__(
        self, historic_average_factor_value_all_assets_handler: HistoricAverageFactorValueAllAssetsHandler, skew_handler: SkewHandler
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.historic_average_factor_value_all_assets_handler = historic_average_factor_value_all_assets_handler
        self.skew_handler = skew_handler

    async def get_demanded_factor_value_async(self, query: GetDemandedFactorValueQuery) -> pd.Series:
        self.logger.info("Fetching demanded factor values for factor %s", query.factor_name)
        demanded_factor_values = (
            await self.historic_average_factor_value_all_assets_handler.get_historic_avg_factor_value_for_all_assets_async(
                factor_name=query.factor_name, lookback=query.lookback
            )
        )
        if query.factor_name == "skew":
            factor_value = await self.skew_handler.get_skew_async(query.symbol, query.lookback)
        elif query.factor_name == "neg_skew":
            factor_value = await self.skew_handler.get_neg_skew_async(query.symbol, query.lookback)
        else:
            raise ValueError("Invalid factor name")
        demean_value = demanded_factor_values.reindex(factor_value.index)
        demean_value = demean_value.ffill()
        return factor_value - demean_value
