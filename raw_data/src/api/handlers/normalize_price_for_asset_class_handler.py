import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository


class NormalizedPriceForAssetClassHandler:
    def __init__(self, instrument_repository: InstrumentsRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository

    async def get_normalized_price_for_asset_class_async(
        self, get_normalized_price_query: NormalizedPriceForAssetClassQuery
    ) -> pd.DataFrame:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {get_normalized_price_query}")
            asset_class = await self.instrument_repository.get_asset_class_async(get_normalized_price_query.symbol)
            instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class.asset_class)
            print(instruments)
            return pd.DataFrame()
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching FX prices: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")
