from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_daily_prices_repository,
    get_db_repository,
    get_instruments_repository,
    get_raw_data_client,
    get_redis,
    get_risk_client,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from common.src.repositories.risk_client import RiskClient
from rules.src.api.handlers.accel_handler import AccelHandler
from rules.src.api.handlers.assettrend_handler import AssettrendHandler
from rules.src.api.handlers.breakout_handler import BreakoutHandler
from rules.src.api.handlers.carry_handler import CarryHandler
from rules.src.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler
from rules.src.api.handlers.momentum_handler import MomentumHandler
from rules.src.api.handlers.rules_manager_handler import RulesManagerHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_rules_handler(repository: Repository = Depends(get_db_repository)) -> RulesManagerHandler:
    return RulesManagerHandler(repository=repository)


def get_momentum_handler(
    prices_repository: PricesClient = Depends(get_daily_prices_repository),
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> MomentumHandler:
    return MomentumHandler(prices_repository=prices_repository, raw_data_client=raw_data_client, redis_repository=redis_repository)


def get_accel_handler(
    momentum_handler: MomentumHandler = Depends(get_momentum_handler),
) -> AccelHandler:
    return AccelHandler(momentum_handler=momentum_handler)


def get_breakout_handler(
    prices_repository: PricesClient = Depends(get_daily_prices_repository),
) -> BreakoutHandler:
    return BreakoutHandler(prices_repository=prices_repository)


def get_asserttrend_handler(
    risk_client: RiskClient = Depends(get_risk_client),
    instrument_repository: InstrumentsClient = Depends(get_instruments_repository),
) -> AssettrendHandler:
    return AssettrendHandler(risk_client=risk_client, instrument_repository=instrument_repository)


def get_carry_handler(raw_data_client: RawDataClient = Depends(get_raw_data_client)) -> CarryHandler:
    return CarryHandler(raw_data_client=raw_data_client)


def get_cs_mean_reversion_handler(
    risk_client: RiskClient = Depends(get_risk_client),
    instrument_repository: InstrumentsClient = Depends(get_instruments_repository),
) -> CSMeanReversionHandler:
    return CSMeanReversionHandler(risk_client=risk_client, instrument_repository=instrument_repository)
