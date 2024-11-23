from grpc import ServicerContext, StatusCode

from common.src.logging.logger import AppLogger
from common.src.protobufs.absolute_skew_deviation_pb2 import AbsoluteSkewDeviationRequest, AbsoluteSkewDeviationResponse
from common.src.protobufs.absolute_skew_deviation_pb2_grpc import (
    AbsoluteSkewDeviationHandlerServicer,
)
from common.src.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import HistoricAverageNegSkewAllAssetsHandler
from raw_data.api.handlers.skew_handler import SkewHandler


class AbsoluteSkewDeviationHandler(AbsoluteSkewDeviationHandlerServicer):
    def __init__(self, historic_negskew_value_all_assets_handler: HistoricAverageNegSkewAllAssetsHandler, skew_handler: SkewHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.historic_negskew_value_all_assets_handler = historic_negskew_value_all_assets_handler
        self.skew_handler = skew_handler

    async def getAbsoluteSkewDeviation(self, request: AbsoluteSkewDeviationRequest, context: ServicerContext):
        try:
            self.logger.info("Fetching absolute skew deviation for symbol: %s", request.symbol)

            if not request.symbol or not request.lookback:
                context.abort(StatusCode.INVALID_ARGUMENT, "Symbol or lookback cannot be empty.")

            historic_avg_neg_skew = await self.historic_negskew_value_all_assets_handler.get_historic_avg_factor_value_for_all_assets_async(
                lookback=request.lookback
            )
            neg_skew = await self.skew_handler.get_neg_skew_async(request.symbol, request.lookback)

            if not context.is_active():
                self.logger.warning("Client canceled the request.")
                return None

            aligned_avg_neg_skew = historic_avg_neg_skew.reindex(neg_skew.index)
            aligned_avg_neg_skew = aligned_avg_neg_skew.ffill()
            abs_skew_deviation = neg_skew - aligned_avg_neg_skew
            response = convert_pandas_to_bytes(abs_skew_deviation)

            return AbsoluteSkewDeviationResponse(series=response)
        except Exception:
            self.logger.exception("Error processing request")
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
