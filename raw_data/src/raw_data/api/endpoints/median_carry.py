from grpc import ServicerContext, StatusCode

from common.logging.logger import AppLogger
from common.protobufs.median_carry_for_asset_class_pb2 import (
    MedianCarryRequest,
    MedianCarryResponse,
)
from common.protobufs.median_carry_for_asset_class_pb2_grpc import MedianCarryServicer
from common.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.median_carry_for_asset_class_handler import MedianCarryForAssetClassHandler


class MedianCarry(MedianCarryServicer):
    def __init__(
        self,
        median_carry_for_asset_class_handler: MedianCarryForAssetClassHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.median_carry_for_asset_class_handler = median_carry_for_asset_class_handler

    async def get_median_carry(self, request: MedianCarryRequest, context: ServicerContext) -> MedianCarryResponse:
        self.logger.info("Fetching median carry for asset class by symbol: %s", request.symbol)

        if not request.symbol:
            self.logger.error("Invalid request: Symbol is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol class cannot be empty.")
            return MedianCarryResponse()

        try:
            results = await self.median_carry_for_asset_class_handler.get_median_carry_for_asset_class_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return MedianCarryResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return MedianCarryResponse()
