from common.logging.logger import AppLogger
from common.protobufs.momentum_pb2 import (
    MomentumRequest,
    MomentumResponse,
)
from common.protobufs.momentum_pb2_grpc import MomentumServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.handlers.momentum_rule_handler import MomentumRuleHandler


class Momentum(MomentumServicer):
    def __init__(
        self,
        momentum_handler: MomentumRuleHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.momentum_handler = momentum_handler

    async def get_momentum(self, request: MomentumRequest, context: ServicerContext) -> MomentumResponse:
        self.logger.info('Fetching Momentum data for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return MomentumResponse()

        try:
            results = await self.momentum_handler.get_momentum_async(
                symbol=request.symbol,
                lfast=request.lfast,
                lslow=request.lslow,
                use_attenuation=request.use_attenuation,
                scaling_factor=request.scaling_factor,
                scaling_type=request.scaling_type,
            )
            response = convert_pandas_to_bytes(results)
            return MomentumResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return MomentumResponse()
