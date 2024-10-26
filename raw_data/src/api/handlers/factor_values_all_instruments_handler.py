import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from raw_data.src.api.handlers.factor_values_over_instrument_list_handler import FactorValuesOverInstrumentListHandler


class FactorValuesAllInstrumentsHandler:
    def __init__(
        self,
        instruments_client: InstrumentsClient,
        factor_values_over_instrument_list_handler: FactorValuesOverInstrumentListHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_client = instruments_client
        self.factor_values_over_instrument_list_handler = factor_values_over_instrument_list_handler

    async def get_factor_values_for_all_instruments_async(self, factor_name: str, lookback: int) -> pd.DataFrame:
        self.logger.info("Fetching factor values for all instruments for factor %s", factor_name)
        instrument_list = await self.instruments_client.get_all_instrument_async()
        return await self.factor_values_over_instrument_list_handler.get_factor_values_over_instrument_list_async(
            instrument_list, factor_name=factor_name, lookback=lookback
        )
