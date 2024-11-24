from grpc import ServicerContext, StatusCode

from common.logging.logger import AppLogger
from common.protobufs.instrument_currency_vol_pb2 import (
    InstrumentCurrencyVolRequest,
    InstrumentCurrencyVolResponse,
)
from common.protobufs.instrument_currency_vol_pb2_grpc import InstrumentCurrencyVolServicer
from common.utils.convertors import convert_pandas_to_bytes
from raw_data.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler


class InstrumentCurrencyVol(InstrumentCurrencyVolServicer):
    def __init__(
        self,
        instrument_currency_vol_handler: InstrumentCurrencyVolHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_currency_vol_handler = instrument_currency_vol_handler

    async def get_instrument_currency_vol(
        self, request: InstrumentCurrencyVolRequest, context: ServicerContext
    ) -> InstrumentCurrencyVolResponse:
        self.logger.info("Fetching instrument currency volatility for instrument: %s", request.symbol)

        if not request.symbol:
            self.logger.error("Invalid request: Symbol is empty.")
            context.abort(StatusCode.INVALID_ARGUMENT, "Symbol cannot be empty.")
            return InstrumentCurrencyVolResponse()

        try:
            results = await self.instrument_currency_vol_handler.get_instrument_currency_vol_async(symbol=request.symbol)
            response = convert_pandas_to_bytes(results)
            return InstrumentCurrencyVolResponse(series=response)

        except Exception as e:
            self.logger.exception("Error processing request: %s", str(e))
            context.abort(StatusCode.INTERNAL, "An unexpected error occurred.")
            return InstrumentCurrencyVolResponse()
