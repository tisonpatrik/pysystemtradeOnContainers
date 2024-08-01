import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from raw_data.src.services.cumulatve_daily_vol_normalized_returns_service import CumulativeDailyVolNormalizedReturnsService
from raw_data.src.services.normalised_price_for_asset_class_service import NormalisedPriceForAssetClassService


class NormalizedPricesForAssetClassHandler:
    def __init__(
        self, instrument_repository: InstrumentsRepository, daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.cumulatve_daily_vol_normalized_returns_service = CumulativeDailyVolNormalizedReturnsService()
        self.normalised_price_for_asset_class_service = NormalisedPriceForAssetClassService()

    async def get_normalized_price_for_asset_class_async(self, query: NormalizedPriceForAssetClassQuery) -> pd.Series:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {query}")
            asset_class = await self.instrument_repository.get_asset_class_async(query.symbol)
            instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class.asset_class)
            aggregated_returns = await self.get_aggregated_returns_across_instruments(instruments)

            norm_returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(query.symbol)
            normalised_price_for_instrument = (
                self.cumulatve_daily_vol_normalized_returns_service.get_cumulative_daily_vol_normalised_returns(norm_returns)
            )
            normalised_price_for_asset = self.normalised_price_for_asset_class_service.get_cumulative_daily_vol_normalised_returns(
                aggregated_returns, normalised_price_for_instrument
            )
            return normalised_price_for_asset

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching normalied prices for asset class: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    async def get_aggregated_returns_across_instruments(self, instruments: list) -> pd.DataFrame:
        aggregate_returns_across_instruments_list = []
        for instrument_code in instruments:
            returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(instrument_code.symbol)
            aggregate_returns_across_instruments_list.append(returns)

        aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)
        return aggregate_returns_across_instruments
