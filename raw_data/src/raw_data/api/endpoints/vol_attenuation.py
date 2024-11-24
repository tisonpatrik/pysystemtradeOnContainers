from grpc import ServicerContext, StatusCode

from common.logging.logger import AppLogger
from common.protobufs.vol_attenuation_pb2 import (
    VolAttenuationRequest,
    VolAttenuationResponse,
)
from common.protobufs.vol_attenuation_pb2_grpc import VolAttenuationServicer
from common.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.vol_attenuation_handler import VolAttenuationHandler


class VolAttenuation(VolAttenuationServicer):
    def __init__(
        self,
        vol_attenuation_handler: VolAttenuationHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.vol_attenuation_handler = vol_attenuation_handler

    async def get_vol_attenuation(self, request: VolAttenuationRequest, context: ServicerContext) -> VolAttenuationResponse:
        self.logger.info("Fetching volume attenuation for symbol: %s", request.symbol)

        if not request.symbol:
            self.logger.error("Invalid request: Symbol is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol cannot be empty.")
            return VolAttenuationResponse()

        try:
            results = await self.vol_attenuation_handler.get_vol_attenuation_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return VolAttenuationResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return VolAttenuationResponse()
