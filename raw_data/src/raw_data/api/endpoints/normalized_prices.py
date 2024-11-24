from grpc import ServicerContext, StatusCode

from common.src.logging.logger import AppLogger
from common.src.protobufs.normalized_prices_pb2 import (
    NormalizedPricesRequest,
    NormalizedPricesResponse,
)
from common.src.protobufs.normalized_prices_pb2_grpc import NormalizedPricesServicer
from common.src.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.normalized_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler


class NormalizedPrices(NormalizedPricesServicer):
    def __init__(
        self,
        normalized_prices_handler: NormalizedPricesForAssetClassHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.normalized_prices_for_asset_class_handler = normalized_prices_handler

    async def get_normalized_prices(self, request: NormalizedPricesRequest, context: ServicerContext) -> NormalizedPricesResponse:
        self.logger.info("Fetching normalized prices for asset class with symbol: %s", request.symbol)

        if not request.symbol:
            self.logger.error("Invalid request: Symbol is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol cannot be empty.")
            return NormalizedPricesResponse()

        try:
            results = await self.normalized_prices_for_asset_class_handler.get_normalized_price_for_asset_class_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return NormalizedPricesResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return NormalizedPricesResponse()
