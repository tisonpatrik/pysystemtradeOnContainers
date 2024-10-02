from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.dependencies.core_dependencies import (
    get_daily_prices_repository,
    get_instruments_repository,
    get_raw_data_client,
    get_redis,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from risk.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from risk.src.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app), setup_async_redis(app), setup_async_client(app):
        yield


async def get_instrument_vol_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    instruments_repository: InstrumentsRepository = Depends(get_instruments_repository),
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(
        prices_repository=prices_repository, instruments_repository=instruments_repository, raw_data_client=raw_data_client
    )


def get_daily_vol_normalized_returns_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(
        prices_repository=prices_repository, raw_data_client=raw_data_client, redis_repository=redis_repository
    )


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsRepository = Depends(get_instruments_repository),
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> AggregatedReturnsForAssetClassHandler:
    return AggregatedReturnsForAssetClassHandler(
        instrument_repository=instrument_repository,
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        redis_repository=redis_repository,
    )


def get_normalized_price_for_asset_class_handler(
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    aggregated_returns_handler: AggregatedReturnsForAssetClassHandler = Depends(get_aggregated_returns_for_asset_class_handler),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        aggregated_returns_for_asset_class_handler=aggregated_returns_handler,
    )
