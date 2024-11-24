from grpc import ServicerContext, StatusCode

from common.logging.logger import AppLogger
from common.protobufs.absolute_skew_deviation_pb2 import (
    AbsoluteSkewDeviationRequest,
    AbsoluteSkewDeviationResponse,
)
from common.protobufs.absolute_skew_deviation_pb2_grpc import AbsoluteSkewDeviationServicer
from common.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.absolute_skew_deviation_handler import AbsoluteSkewDeviationHandler


class AbsoluteSkewDeviation(AbsoluteSkewDeviationServicer):
    def __init__(
        self,
        absolute_skew_deviation_handler: AbsoluteSkewDeviationHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.absolute_skew_deviation_handler = absolute_skew_deviation_handler

    async def get_absolute_skew_deviation(
        self, request: AbsoluteSkewDeviationRequest, context: ServicerContext
    ) -> AbsoluteSkewDeviationResponse:
        self.logger.info("Fetching absolute skew deviation for symbol: %s", request.symbol)

        if not request.symbol or not request.lookback:
            self.logger.error("Invalid request: Symbol or lookback is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol or lookback cannot be empty.")
            return AbsoluteSkewDeviationResponse()

        try:
            results = await self.absolute_skew_deviation_handler.get_absolute_skew_deviation_async(
                symbol=request.symbol, lookback=request.lookback
            )
            response = convert_pandas_to_bytes(results)
            return AbsoluteSkewDeviationResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return AbsoluteSkewDeviationResponse()
