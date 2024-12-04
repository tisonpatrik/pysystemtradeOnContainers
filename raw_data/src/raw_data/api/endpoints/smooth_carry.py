from common.logging.logger import AppLogger
from common.protobufs.raw_data_pb2 import (
    SmoothCarryRequest,
    SmoothCarryResponse,
)
from common.protobufs.raw_data_pb2_grpc import SmoothCarryServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from raw_data.api.handlers.smooth_carry_handler import SmoothCarryHandler


class SmoothCarry(SmoothCarryServicer):
    def __init__(
        self,
        smooth_carry_handler: SmoothCarryHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.smooth_carry_handler = smooth_carry_handler

    async def get_smooth_carry(self, request: SmoothCarryRequest, context: ServicerContext) -> SmoothCarryResponse:
        self.logger.info('Fetching smooth carry data for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol cannot be empty.')
            return SmoothCarryResponse()

        try:
            results = await self.smooth_carry_handler.get_smooth_carry_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return SmoothCarryResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return SmoothCarryResponse()
