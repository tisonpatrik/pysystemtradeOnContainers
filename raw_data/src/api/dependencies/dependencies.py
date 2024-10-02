from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_daily_prices_repository, get_db_repository, get_raw_data_client
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from raw_data.src.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.src.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.api.handlers.raw_carry_handler import RawCarryHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_fx_prices_handler(repository: Repository = Depends(get_db_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)


def get_annualised_roll_handler(prices_repository: PricesRepository = Depends(get_daily_prices_repository)) -> DailyAnnualisedRollHandler:
    return DailyAnnualisedRollHandler(prices_repository=prices_repository)


def get_raw_carry_handler(
    daily_annualised_roll_handler: DailyAnnualisedRollHandler = Depends(get_annualised_roll_handler),
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> RawCarryHandler:
    return RawCarryHandler(daily_annualised_roll_handler=daily_annualised_roll_handler, raw_data_client=raw_data_client)


async def get_daily_returns_vol_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(prices_repository=prices_repository)
