import asyncio

import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.utils.bounded_task_group import BoundedTaskGroup
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class AggregatedReturnsForAssetClassHandler:
    def __init__(
        self,
        instrument_repository: InstrumentsClient,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.max_concurrent_tasks = 8

    async def get_aggregated_returns_for_asset_async(self, asset_class: str) -> pd.Series:
        self.logger.info("Fetching aggregated returns for asset class %s", asset_class)
        instruments = await self._get_instruments_for_asset_class(asset_class)
        aggregate_returns = await self._fetch_returns_for_instruments(instruments)
        return self._calculate_median_returns(aggregate_returns)

    async def _get_instruments_for_asset_class(self, asset_class: str) -> list:
        instruments = await self.instrument_repository.get_tradable_instruments_for_asset_class_async(asset_class)
        if not instruments:
            self.logger.warning("No instruments found for asset class: %s", asset_class)
            raise ValueError(f"No instruments found for asset class: {asset_class}")
        return instruments

    async def _fetch_returns_for_instruments(self, instruments: list) -> list:
        aggregate_returns = []
        async with BoundedTaskGroup(max_parallelism=self.max_concurrent_tasks) as tg:
            tasks = [tg.create_task(self._fetch_return_for_instrument(instrument)) for instrument in instruments]
            results = await asyncio.gather(*tasks)
            aggregate_returns = [res for res in results if res is not None]

        if not aggregate_returns:
            raise ValueError("No returns data found for instruments")
        return aggregate_returns

    async def _fetch_return_for_instrument(self, instrument) -> pd.Series:
        try:
            self.logger.info("Fetching returns for instrument: %s", instrument.symbol)
            return await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns_async(instrument.symbol)
        except Exception as e:
            self.logger.exception("Error fetching returns for instrument: %s", instrument.symbol)
            raise RuntimeError(f"Failed to fetch returns for instrument {instrument.symbol}") from e

    def _calculate_median_returns(self, aggregate_returns: list) -> pd.Series:
        aggregated_data = pd.concat(aggregate_returns, axis=1)
        return aggregated_data.median(axis=1)
