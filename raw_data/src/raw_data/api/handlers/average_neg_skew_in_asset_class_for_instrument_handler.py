import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.logging.logger import AppLogger
from raw_data.api.handlers.current_average_negskew_over_asset_class_handler import CurrentAverageNegSkewOverAssetClassHandler


class AverageNegSkewInAssetClassForInstrumentHandler:
    def __init__(
        self,
        instruments_client: InstrumentsClient,
        current_average_negskew_over_asset_class_handler: CurrentAverageNegSkewOverAssetClassHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instruments_client = instruments_client
        self.current_average_negskew_over_asset_class_handler = current_average_negskew_over_asset_class_handler

    async def get_average_negskew_in_asset_class_for_instrument_async(self, symbol: str, lookback: int) -> pd.Series:
        self.logger.info("Fetching negskew in asset class for instrument: %s", symbol)
        asset_class = await self.instruments_client.get_asset_class_async(symbol)
        return await self.current_average_negskew_over_asset_class_handler.current_average_negskew_over_asset_class_async(
            asset_class, lookback=lookback
        )
