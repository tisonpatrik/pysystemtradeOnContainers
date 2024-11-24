from grpc import ServicerContext, StatusCode

from common.src.logging.logger import AppLogger
from common.src.protobufs.raw_carry_pb2 import (
    RawCarryRequest,
    RawCarryResponse,
)
from common.src.protobufs.raw_carry_pb2_grpc import RawCarryServicer
from common.src.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.raw_carry_handler import RawCarryHandler


class RawCarry(RawCarryServicer):
    def __init__(
        self,
        raw_carry_handler: RawCarryHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_carry_handler = raw_carry_handler

    async def get_raw_carry(self, request: RawCarryRequest, context: ServicerContext) -> RawCarryResponse:
        self.logger.info("Fetching raw carry data for symbol: %s", request.symbol)

        if not request.symbol:
            self.logger.error("Invalid request: Symbol is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol cannot be empty.")
            return RawCarryResponse()

        try:
            results = await self.raw_carry_handler.get_raw_carry_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return RawCarryResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return RawCarryResponse()
