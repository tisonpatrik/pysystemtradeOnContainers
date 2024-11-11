import pandas as pd

from common.src.cqrs.api_queries.get_absolute_skew_deviation import GetAbsoluteSkewDeviationQuery
from common.src.logging.logger import AppLogger
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import HistoricAverageNegSkewAllAssetsHandler
from raw_data.api.handlers.skew_handler import SkewHandler


class AbsoluteSkewDeviationHandler:
    def __init__(self, historic_negskew_value_all_assets_handler: HistoricAverageNegSkewAllAssetsHandler, skew_handler: SkewHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.historic_negskew_value_all_assets_handler = historic_negskew_value_all_assets_handler
        self.skew_handler = skew_handler

    async def get_absolute_skew_deviation_async(self, query: GetAbsoluteSkewDeviationQuery) -> pd.Series:
        self.logger.info("Fetching absolute skew deviaton for symbol: %s", query.symbol)
        historic_avg_neg_skew = await self.historic_negskew_value_all_assets_handler.get_historic_avg_factor_value_for_all_assets_async(
            lookback=query.lookback
        )
        neg_skew = await self.skew_handler.get_neg_skew_async(query.symbol, query.lookback)
        aligned_avg_neg_skew = historic_avg_neg_skew.reindex(neg_skew.index)
        aligned_avg_neg_skew = aligned_avg_neg_skew.ffill()
        return neg_skew - aligned_avg_neg_skew
