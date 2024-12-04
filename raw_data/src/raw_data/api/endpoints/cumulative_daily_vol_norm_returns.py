from common.logging.logger import AppLogger
from common.protobufs.raw_data_pb2 import (
    CumulativeDailyVolNormReturnsRequest,
    CumulativeDailyVolNormReturnsResponse,
)
from common.protobufs.raw_data_pb2_grpc import CumulativeDailyVolNormReturnsServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler


class CumulativeDailyVolNormReturns(CumulativeDailyVolNormReturnsServicer):
    def __init__(
        self,
        cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.cumulative_daily_vol_norm_returns_handler = cumulative_daily_vol_norm_returns_handler

    async def get_cumulative_daily_vol_norm_returns(
        self, request: CumulativeDailyVolNormReturnsRequest, context: ServicerContext
    ) -> CumulativeDailyVolNormReturnsResponse:
        self.logger.info('Fetching cumulative daily vol normalized returns for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol cannot be empty.')
            return CumulativeDailyVolNormReturnsResponse()

        try:
            results = await self.cumulative_daily_vol_norm_returns_handler.get_cumulative_daily_vol_norm_returns_async(
                symbol=request.symbol
            )
            response = convert_pandas_to_bytes(results)
            return CumulativeDailyVolNormReturnsResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return CumulativeDailyVolNormReturnsResponse()
