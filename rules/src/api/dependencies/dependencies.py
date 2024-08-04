from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_client,
    get_daily_prices_repository,
    get_raw_data_client,
    get_repository,
    get_risk_client,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.http_client.rest_client import RestClient
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from common.src.repositories.risk_client import RiskClient
from rules.src.api.handlers.accel_handler import AccelHandler
from rules.src.api.handlers.assettrend_handler import AssettrendHandler
from rules.src.api.handlers.breakout_handler import BreakoutHandler
from rules.src.api.handlers.rules_manager_handler import RulesManagerHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_rules_handler(repository: Repository = Depends(get_repository)) -> RulesManagerHandler:
    return RulesManagerHandler(repository=repository)


def get_accel_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    risk_client: RiskClient = Depends(get_risk_client),
) -> AccelHandler:
    return AccelHandler(prices_repository=prices_repository, risk_client=risk_client)


def get_breakout_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    client: RestClient = Depends(get_client),
) -> BreakoutHandler:
    return BreakoutHandler(prices_repository=prices_repository, client=client)


def get_asserttrend_handler(raw_data_client: RawDataClient = Depends(get_raw_data_client)) -> AssettrendHandler:
    return AssettrendHandler(raw_data_client=raw_data_client)
