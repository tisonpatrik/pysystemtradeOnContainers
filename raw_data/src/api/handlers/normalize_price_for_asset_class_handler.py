import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class NormalizedPriceForAssetClassHandler:
    def __init__(
        self, instrument_repository: InstrumentsRepository, daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler

    async def get_normalized_price_for_asset_class_async(self, get_normalized_price_query: NormalizedPriceForAssetClassQuery) -> pd.Series:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {get_normalized_price_query}")
            asset_class = await self.instrument_repository.get_asset_class_async(get_normalized_price_query.symbol)
            instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class.asset_class)
            normalised_price_for_asset_class = await self.daily_vol_normalised_price_for_list_of_instruments(instruments)
            normalised_price_this_instrument = await self.get_cumulative_daily_vol_normalised_returns(get_normalized_price_query.symbol)
            normalised_price_for_asset_class_aligned = normalised_price_for_asset_class.reindex(
                normalised_price_this_instrument.index
            ).ffill()
            return normalised_price_for_asset_class_aligned
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching FX prices: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    async def daily_vol_normalised_price_for_list_of_instruments(self, list_of_instruments: list) -> pd.Series:
        aggregate_returns_across_instruments_list = []
        for instrument_code in list_of_instruments:
            returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(instrument_code)
            aggregate_returns_across_instruments_list.append(returns)

        aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)
        norm_returns = aggregate_returns_across_instruments.median(axis=1)
        norm_price = norm_returns.cumsum()
        return norm_price

    async def get_cumulative_daily_vol_normalised_returns(self, instrument_code: str) -> pd.Series:
        norm_returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(instrument_code)
        cum_norm_returns = norm_returns.cumsum()
        return cum_norm_returns
