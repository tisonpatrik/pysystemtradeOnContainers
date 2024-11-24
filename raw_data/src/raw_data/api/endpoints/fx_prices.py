from grpc import ServicerContext, StatusCode

from common.src.logging.logger import AppLogger
from common.src.protobufs.fx_prices_pb2 import FxPricesRequest, FxPricesResponse
from common.src.protobufs.fx_prices_pb2_grpc import FxPricesServicer
from common.src.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.fx_prices_handler import FxPricesHandler


class FxPrices(FxPricesServicer):
    def __init__(
        self,
        fx_prices_handler: FxPricesHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.fx_prices_handler = fx_prices_handler

    async def get_fx_prices(self, request: FxPricesRequest, context: ServicerContext) -> FxPricesResponse:
        self.logger.info("Fetching FX prices for symbol %s with base currency %s", request.symbol, request.base_currency)

        if not request.symbol or not request.base_currency:
            self.logger.error("Invalid request: Symbol or base currency is empty.")
            context.abort(
                StatusCode.INVALID_ARGUMENT, "Symbol: %s or base currency: % cannot be empty.", request.symbol, request.base_currency
            )
            return FxPricesResponse()
        try:
            fx_data = await self.fx_prices_handler.get_fx_prices(request.symbol, request.base_currency)
            results = convert_pandas_to_bytes(fx_data)
            return FxPricesResponse(series=results)
        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return FxPricesResponse()
