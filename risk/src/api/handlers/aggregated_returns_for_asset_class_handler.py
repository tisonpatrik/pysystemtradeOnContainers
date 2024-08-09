import pandas as pd

from common.src.cqrs.cache_queries.aggregated_returns_for_asset_class_cache import (
    GetAggregatedReturnsForAssetClassCache,
    SetAggregatedReturnsForAssetClassCache,
)
from common.src.logging.logger import AppLogger
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.utils.convertors import convert_cache_to_series
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from risk.src.validation.aggregated_returns_for_asset_class import AggregatedReturnsForAssetClass


class AggregatedReturnsForAssetClassHandler:
    def __init__(self,
        instrument_repository: InstrumentsRepository,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
        redis_repository: RedisRepository):

        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler
        self.redis_repository = redis_repository


    async def get_aggregated_returns_for_asset_class_async(self, asset_class: str) -> pd.Series:
            self.logger.info(f"Fetching instruments for asset class: {asset_class}")
            cache_statement = GetAggregatedReturnsForAssetClassCache(asset_class)
            try:
                cached_data = await self.redis_repository.get_cache(cache_statement)
                if cached_data is not None:
                    series = convert_cache_to_series(cached_data,
                        AggregatedReturnsForAssetClass,
                        str(AggregatedReturnsForAssetClass.date_time),
                        str(AggregatedReturnsForAssetClass.price))
                    return series

                instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class)

                if not instruments:
                    self.logger.warning(f"No instruments found for asset class: {asset_class}")
                    raise ValueError(f"No instruments found for asset class: {asset_class}")

                aggregate_returns_across_instruments_list = []

                for instrument_code in instruments:
                    try:
                        self.logger.info(f"Fetching returns for instrument: {instrument_code.symbol}")
                        returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(instrument_code.symbol)
                        aggregate_returns_across_instruments_list.append(returns)
                    except Exception as e:
                        self.logger.error(f"Error fetching returns for instrument {instrument_code.symbol}: {e}")

                if not aggregate_returns_across_instruments_list:
                    self.logger.warning(f"No returns data found for asset class: {asset_class}")
                    raise ValueError(f"No returns data found for asset class: {asset_class}")

                aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)

                median_returns = aggregate_returns_across_instruments.median(axis=1)
                self.logger.info(f"Successfully aggregated returns for asset class: {asset_class}")
                cache_set_statement = SetAggregatedReturnsForAssetClassCache(
                    returns=median_returns,
                    asset_class=asset_class
                )
                await self.redis_repository.set_cache(cache_set_statement)
                return median_returns

            except Exception as e:
                self.logger.error(f"Error in get_aggregated_returns_across_instruments for asset class {asset_class}: {e}")
                raise ValueError(f"Error processing returns for asset class {asset_class}: {e}")
