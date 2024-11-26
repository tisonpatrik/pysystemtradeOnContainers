from common.logging.logger import AppLogger
from common.protobufs.cs_mean_reversion_pb2 import (
    CSMeanReversionRequest,
    CSMeanReversionResponse,
)
from common.protobufs.cs_mean_reversion_pb2_grpc import CSMeanReversionServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler


class CSMeanReversion(CSMeanReversionServicer):
    def __init__(
        self,
        csmeanreversion_handler: CSMeanReversionHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.csmeanreversion_handler = csmeanreversion_handler

    async def get_cs_mean_reversion(self, request: CSMeanReversionRequest, context: ServicerContext) -> CSMeanReversionResponse:
        self.logger.info('Fetching CSMeanReversion data for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol or lookback is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol or lookback cannot be empty.')
            return CSMeanReversionResponse()

        try:
            results = await self.csmeanreversion_handler.get_cs_mean_reversion_async(
                symbol=request.symbol,
                horizon=request.horizon,
                use_attenuation=request.use_attenuation,
                scaling_factor=request.scaling_factor,
                scaling_type=request.scaling_type,
            )
            response = convert_pandas_to_bytes(results)
            return CSMeanReversionResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return CSMeanReversionResponse()
