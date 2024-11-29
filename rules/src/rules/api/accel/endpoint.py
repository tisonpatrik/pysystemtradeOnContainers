from common.logging.logger import AppLogger
from common.protobufs.accel_pb2 import (
    AccelRequest,
    AccelResponse,
)
from common.protobufs.accel_pb2_grpc import AccelServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.accel.handler import AccelHandler
from rules.api.accel.request import AccelQuery


class Accel(AccelServicer):
    def __init__(
        self,
        accel_handler: AccelHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_handler = accel_handler

    async def get_accel(self, request: AccelRequest, context: ServicerContext) -> AccelResponse:
        self.logger.info('Fetching absolute skew deviation for symbol: %s', request.symbol)
        query = AccelQuery(
            symbol=request.symbol,
            lfast=request.lfast,
            use_attenuation=request.use_attenuation,
            scaling_factor=request.scaling_factor,
            scaling_type=request.scaling_type,
        )
        try:
            results = await self.accel_handler.get_accel_async(query)
            response = convert_pandas_to_bytes(results)
            return AccelResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return AccelResponse()
