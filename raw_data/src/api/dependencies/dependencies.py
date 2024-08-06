from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_daily_prices_repository,
    get_instruments_repository,
    get_repository,
    get_risk_client,
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


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_fx_prices_handler(repository: Repository = Depends(get_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)


def get_daily_vol_normalized_returns_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    risk_client: RiskClient = Depends(get_risk_client),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(prices_repository=prices_repository, risk_client=risk_client)


def get_normalized_price_for_asset_class_handler(
    instrument_repository: InstrumentsRepository = Depends(get_instruments_repository),
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        instrument_repository=instrument_repository, daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler
    )
