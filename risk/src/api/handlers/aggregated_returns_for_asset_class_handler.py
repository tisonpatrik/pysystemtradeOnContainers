import asyncio

import pandas as pd

from common.src.cqrs.cache_queries.aggregated_returns_for_asset_class_cache import (
    GetAggregatedReturnsForAssetClassCache,
    SetAggregatedReturnsForAssetClassCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from risk.src.validation.aggregated_returns_for_asset_class import AggregatedReturnsForAssetClass


class AggregatedReturnsForAssetClassHandler:
    def __init__(
        self,
        instrument_repository: InstrumentsRepository,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
        redis_repository: RedisRepository,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.redis_repository = redis_repository

    async def get_aggregated_returns_for_asset_class_async(self, asset_class: str) -> pd.Series:
        cache_statement = GetAggregatedReturnsForAssetClassCache(asset_class)
        try:
            cached_data = await self.redis_repository.get_cache(cache_statement)
            if cached_data is not None:
                return AggregatedReturnsForAssetClass.from_cache_to_series(cached_data)

            instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class)

            if not instruments:
                self.logger.warning("No instruments found for asset class: %s", asset_class)
                raise ValueError(f"No instruments found for asset class: {asset_class}")

            aggregate_returns_across_instruments_list = []

            for instrument_code in instruments:
                try:
                    self.logger.info("Fetching returns for instrument: %s", instrument_code.symbol)
                    returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns(instrument_code.symbol)
                    if returns is not None:
                        aggregate_returns_across_instruments_list.append(returns)
                except Exception:
                    self.logger.exception("Error fetching returns for instrument %s", instrument_code.symbol)

            if not aggregate_returns_across_instruments_list:
                self.logger.warning("No returns data found for asset class: %s", asset_class)
                raise ValueError(f"No returns data found for asset class: {asset_class}")

            aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)

            median_returns = aggregate_returns_across_instruments.median(axis=1)
            self.logger.info("Successfully aggregated returns for asset class: %s", asset_class)

            cache_set_statement = SetAggregatedReturnsForAssetClassCache(returns=median_returns, asset_class=asset_class)
            cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))
            cache_task.add_done_callback(lambda t: self.logger.info("Cache set task completed"))

            return median_returns

        except Exception:
            self.logger.exception("Error in get_aggregated_returns_across_instruments for asset class: %s", asset_class)
            raise
