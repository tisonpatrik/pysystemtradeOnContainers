import asyncio

import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.logging.logger import AppLogger
from common.src.utils.bounded_task_group import BoundedTaskGroup
from raw_data.old_api.handlers.raw_carry_handler import RawCarryHandler


class MedianCarryForAssetClassHandler:
    def __init__(self, raw_carry_handler: RawCarryHandler, instrument_client: InstrumentsClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_carry_handler = raw_carry_handler
        self.instrument_client = instrument_client
        self.max_concurrent_tasks = 8

    async def get_median_carry_for_asset_class_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching Median Carry For Asset Class for symbol %s", symbol)
        carry = await self.raw_carry_handler.get_raw_carry_async(symbol)
        asset_class = await self.instrument_client.get_asset_class_async(symbol=symbol)
        raw_median_carry = await self._by_asset_class_median_carry_for_asset_class(asset_class)
        return raw_median_carry.reindex(carry.index).ffill()

    async def _by_asset_class_median_carry_for_asset_class(self, asset_class: str, smooth_days=90) -> pd.Series:
        instruments_in_asset_class = await self.instrument_client.get_tradable_instruments_for_asset_class_async(asset_class)
        raw_carry_across_asset_class = []

        async with BoundedTaskGroup(max_parallelism=self.max_concurrent_tasks) as tg:
            tasks = [tg.create_task(self._fetch_raw_carry(instrument.symbol)) for instrument in instruments_in_asset_class]
            raw_carry_across_asset_class = await asyncio.gather(*tasks)

        # Build DataFrame from the results
        raw_carry_across_asset_class_pd = pd.concat(raw_carry_across_asset_class, axis=1)
        smoothed_carrys_across_asset_class = raw_carry_across_asset_class_pd.ewm(smooth_days).mean()
        return smoothed_carrys_across_asset_class.median(axis=1)

    async def _fetch_raw_carry(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Fetching raw carry for symbol: %s", symbol)
            return await self.raw_carry_handler.get_raw_carry_async(symbol)
        except Exception as e:
            self.logger.exception("Error fetching raw carry for symbol: %s", symbol)
            raise RuntimeError(f"Failed to fetch raw carry for symbol {symbol}") from e
