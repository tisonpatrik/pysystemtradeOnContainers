from common.logging.logger import AppLogger
from common.protobufs.raw_data_pb2 import (
    DailyReturnsVolRequest,
    DailyReturnsVolResponse,
)
from common.protobufs.raw_data_pb2_grpc import DailyReturnsVolServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler


class DailyReturnsVol(DailyReturnsVolServicer):
    def __init__(
        self,
        daily_returns_vol_handler: DailyReturnsVolHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_handler = daily_returns_vol_handler

    async def get_daily_returns_vol(self, request: DailyReturnsVolRequest, context: ServicerContext) -> DailyReturnsVolResponse:
        self.logger.info('Fetching absolute skew deviation for symbol: %s', request.symbol)

        if not request.symbol:
            self.logger.error('Invalid request: Symbol is empty.')
            context.abort(StatusCode.INVALID_ARGUMENT, 'Symbol cannot be empty.')
            return DailyReturnsVolResponse()

        try:
            results = await self.daily_returns_vol_handler.get_daily_returns_vol_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return DailyReturnsVolResponse(series=response)

        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return DailyReturnsVolResponse()
