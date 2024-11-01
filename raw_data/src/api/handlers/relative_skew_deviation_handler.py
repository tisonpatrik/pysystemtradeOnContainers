import pandas as pd

from common.src.cqrs.api_queries.get_relative_skew_deviation import GetRelativeSkewDeviationQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.average_neg_skew_in_asset_class_for_instrument_handler import AverageNegSkewInAssetClassForInstrumentHandler
from raw_data.src.api.handlers.skew_handler import SkewHandler


class RelativeSkewDeviationHandler:
    def __init__(
        self,
        average_neg_skew_in_asset_class_for_instrument_handler: AverageNegSkewInAssetClassForInstrumentHandler,
        skew_handler: SkewHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.average_neg_skew_in_asset_class_for_instrument_handler = average_neg_skew_in_asset_class_for_instrument_handler
        self.skew_handler = skew_handler

    async def get_relative_skew_deviation_async(self, query: GetRelativeSkewDeviationQuery) -> pd.Series:
        self.logger.info("Fetching relative skew deviation for symbol: %s", query.symbol)
        relative_avg_neg_skew = (
            await self.average_neg_skew_in_asset_class_for_instrument_handler.get_average_negskew_in_asset_class_for_instrument_async(
                symbol=query.symbol, lookback=query.lookback
            )
        )
        neg_skew = await self.skew_handler.get_neg_skew_async(query.symbol, query.lookback)
        aligned_avg_neg_skew = relative_avg_neg_skew.reindex(neg_skew.index)
        aligned_avg_neg_skew = aligned_avg_neg_skew.ffill()
        return neg_skew - aligned_avg_neg_skew
