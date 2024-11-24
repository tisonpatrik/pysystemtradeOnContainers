import pandas as pd

from common.clients.instruments_client import InstrumentsClient
from common.logging.logger import AppLogger
from raw_data.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler


class CurrentAverageNegSkewOverAssetClassHandler:
    def __init__(
        self,
        instruments_client: InstrumentsClient,
        negskew_over_instrument_list_handler: NegSkewOverInstrumentListHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_client = instruments_client
        self.negskew_over_instrument_list_handler = negskew_over_instrument_list_handler

    async def current_average_negskew_over_asset_class_async(self, asset: str, lookback: int) -> pd.Series:
        self.logger.info("Fetching current average negskew over asset class")
        instrument_list = await self.instruments_client.get_all_instruments_for_asset_class_async(asset)
        all_factor_values = await self.negskew_over_instrument_list_handler.get_negskew_over_instrument_list_async(
            instrument_list, lookback=lookback
        )
        return all_factor_values.ffill().mean(axis=1)
