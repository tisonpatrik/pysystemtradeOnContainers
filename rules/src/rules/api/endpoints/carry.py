from common.logging.logger import AppLogger
from common.protobufs.carry_pb2 import (
    CarryRequest,
    CarryResponse,
)
from common.protobufs.carry_pb2_grpc import CarryServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.handlers.carry_handler import CarryHandler


class Carry(CarryServicer):
    def __init__(
        self,
        carry_handler: CarryHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_handler = carry_handler

    async def get_carry(self, request: CarryRequest, context: ServicerContext) -> CarryResponse:
        self.logger.info('Fetching carry data for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return CarryResponse()

        try:
            results = await self.carry_handler.get_carry_async(
                symbol=request.symbol,
                smooth_days=request.smooth_days,
                use_attenuation=request.use_attenuation,
                scaling_factor=request.scaling_factor,
                scaling_type=request.scaling_type,
            )
            response = convert_pandas_to_bytes(results)
            return CarryResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return CarryResponse()
