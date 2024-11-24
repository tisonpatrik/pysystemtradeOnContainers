import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.logging.logger import AppLogger
from raw_data.old_api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler


class NegSkewAllInstrumentsHandler:
    def __init__(
        self,
        instruments_client: InstrumentsClient,
        negskew_over_instrument_list_handler: NegSkewOverInstrumentListHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_client = instruments_client
        self.negskew_over_instrument_list_handler = negskew_over_instrument_list_handler

    async def get_negskew_for_all_instruments_async(self, lookback: int) -> pd.DataFrame:
        self.logger.info("Fetching factor values for all instruments")
        instrument_list = await self.instruments_client.get_tradable_instrument_async()
        return await self.negskew_over_instrument_list_handler.get_negskew_over_instrument_list_async(instrument_list, lookback=lookback)
