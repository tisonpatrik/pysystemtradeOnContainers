import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from raw_data.src.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler


class CurrentAverageNegSkewOverAssetClassHandler:
    def __init__(
        self,
        instruments_repository: InstrumentsClient,
        negskew_over_instrument_list_handler: NegSkewOverInstrumentListHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_repository = instruments_repository
        self.negskew_over_instrument_list_handler = negskew_over_instrument_list_handler

    async def current_average_negskew_over_asset_class_async(self, asset: str, lookback: int) -> pd.Series:
        self.logger.info("Fetching current average negskew over asset class")
        instrument_list = await self.instruments_repository.get_instruments_for_asset_class_async(asset)

        all_factor_values = await self.negskew_over_instrument_list_handler.get_factor_values_over_instrument_list_async(
            instrument_list, lookback=lookback
        )
        return all_factor_values.ffill().mean(axis=1)
