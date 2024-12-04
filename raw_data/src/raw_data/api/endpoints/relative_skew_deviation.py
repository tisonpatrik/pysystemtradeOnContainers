from common.logging.logger import AppLogger
from common.protobufs.raw_data_pb2 import (
    RelativeSkewDeviationRequest,
    RelativeSkewDeviationResponse,
)
from common.protobufs.raw_data_pb2_grpc import RelativeSkewDeviationServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from raw_data.api.handlers.relative_skew_deviation_handler import RelativeSkewDeviationHandler


class RelativeSkewDeviation(RelativeSkewDeviationServicer):
    def __init__(
        self,
        relative_skew_deviation_handler: RelativeSkewDeviationHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.relative_skew_deviation_handler = relative_skew_deviation_handler

    async def get_relative_skew_deviation(
        self, request: RelativeSkewDeviationRequest, context: ServicerContext
    ) -> RelativeSkewDeviationResponse:
        self.logger.info('Fetching relative skew deviation for symbol: %s', request.symbol)

        if not request.symbol or not request.lookback:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return RelativeSkewDeviationResponse()

        try:
            results = await self.relative_skew_deviation_handler.get_relative_skew_deviation_async(
                symbol=request.symbol, lookback=request.lookback
            )
            response = convert_pandas_to_bytes(results)
            return RelativeSkewDeviationResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return RelativeSkewDeviationResponse()
