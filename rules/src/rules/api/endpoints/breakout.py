from common.logging.logger import AppLogger
from common.protobufs.breakout_pb2 import (
    BreakoutRequest,
    BreakoutResponse,
)
from common.protobufs.breakout_pb2_grpc import BreakoutServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.handlers.breakout_handler import BreakoutHandler


class Breakout(BreakoutServicer):
    def __init__(
        self,
        breakout_handler: BreakoutHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.breakout_handler = breakout_handler

    async def get_breakout(self, request: BreakoutRequest, context: ServicerContext) -> BreakoutResponse:
        self.logger.info('Fetching breakout data for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return BreakoutResponse()

        try:
            results = await self.breakout_handler.get_breakout_async(
                symbol=request.symbol,
                lookback=request.lookback,
                use_attenuation=request.use_attenuation,
                scaling_factor=request.scaling_factor,
                scaling_type=request.scaling_type,
            )
            response = convert_pandas_to_bytes(results)
            return BreakoutResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return BreakoutResponse()
