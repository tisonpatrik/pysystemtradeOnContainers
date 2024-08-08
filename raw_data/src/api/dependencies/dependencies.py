from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_daily_prices_repository,
    get_instruments_repository,
    get_db_repository,
    get_risk_client,
    get_redis,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.risk_client import RiskClient
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler
from raw_data.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from common.src.redis.redis_repository import RedisRepository

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_fx_prices_handler(repository: Repository = Depends(get_db_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)


def get_daily_vol_normalized_returns_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    risk_client: RiskClient = Depends(get_risk_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(
        prices_repository=prices_repository,
        risk_client=risk_client,
        redis_repository=redis_repository)


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsRepository = Depends(get_instruments_repository),
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> AggregatedReturnsForAssetClassHandler:
    return AggregatedReturnsForAssetClassHandler(
        instrument_repository=instrument_repository,
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        redis_repository=redis_repository
    )

def get_normalized_price_for_asset_class_handler(
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    aggregated_returns_for_asset_class_handler: AggregatedReturnsForAssetClassHandler = Depends(get_aggregated_returns_for_asset_class_handler),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        aggregated_returns_for_asset_class_handler=aggregated_returns_for_asset_class_handler
    )
