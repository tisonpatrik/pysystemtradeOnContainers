from common.logging.logger import AppLogger
from common.protobufs.asserttrend_pb2 import (
    AssertTrendRequest,
    AssertTrendResponse,
)
from common.protobufs.asserttrend_pb2_grpc import AssertTrendServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.handlers.asserttrend_handler import AssertTrendHandler


class AssertTrend(AssertTrendServicer):
    def __init__(
        self,
        asserttrend_handler: AssertTrendHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.asserttrend_handler = asserttrend_handler

    async def get_asserttrend(self, request: AssertTrendRequest, context: ServicerContext) -> AssertTrendResponse:
        self.logger.info('Fetching absolute skew deviation for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return AssertTrendResponse()

        try:
            results = await self.asserttrend_handler.get_asserttrend_async(
                symbol=request.symbol,
                lfast=request.lfast,
                lslow=request.lslow,
                use_attenuation=request.use_attenuation,
                scaling_factor=request.scaling_factor,
                scaling_type=request.scaling_type,
            )
            response = convert_pandas_to_bytes(results)
            return AssertTrendResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return AssertTrendResponse()
