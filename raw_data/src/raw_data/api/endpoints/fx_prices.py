from common.logging.logger import AppLogger
from common.protobufs.raw_data_pb2 import FxPricesRequest, FxPricesResponse
from common.protobufs.raw_data_pb2_grpc import FxPricesServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from raw_data.api.handlers.fx_prices_handler import FxPricesHandler


class FxPrices(FxPricesServicer):
    def __init__(
        self,
        fx_prices_handler: FxPricesHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.fx_prices_handler = fx_prices_handler

    async def get_fx_prices(self, request: FxPricesRequest, context: ServicerContext) -> FxPricesResponse:
        self.logger.info('Fetching FX prices for symbol %s with base currency %s', request.symbol, request.base_currency)

        if not request.symbol or not request.base_currency:
            self.logger.error('Symbol: %s or base currency: %s cannot be empty.', request.symbol, request.base_currency)
            context.abort(code=StatusCode.INVALID_ARGUMENT, details='Invalid request: Symbol or base currency is empty.')
            return FxPricesResponse()
        try:
            fx_data = await self.fx_prices_handler.get_fx_prices(request.symbol, request.base_currency)
            results = convert_pandas_to_bytes(fx_data)
            return FxPricesResponse(series=results)
        except Exception as e:
            self.logger.exception('Error processing request: %s', str(e))
            context.abort(StatusCode.INTERNAL, 'An unexpected error occurred.')
            return FxPricesResponse()
