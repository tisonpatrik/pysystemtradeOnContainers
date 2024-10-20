from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_carry_repository,
    get_daily_prices_repository,
    get_db_repository,
    get_raw_data_client,
    get_redis,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.carry_client import CarryClient
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.api.handlers.accel_handler import AccelHandler
from rules.src.api.handlers.assettrend_handler import AssettrendHandler
from rules.src.api.handlers.breakout_handler import BreakoutHandler
from rules.src.api.handlers.carry_handler import CarryHandler
from rules.src.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler
from rules.src.api.handlers.momentum_handler import MomentumHandler
from rules.src.api.handlers.relative_carry_handler import RelativeCarryHandler
from rules.src.api.handlers.relative_momentum_handler import RelativeMomentumHandler
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
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> AssettrendHandler:
    return AssettrendHandler(raw_data_client=raw_data_client)


def get_carry_handler(carry_client: CarryClient = Depends(get_carry_repository)) -> CarryHandler:
    return CarryHandler(carry_client=carry_client)


def get_cs_mean_reversion_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> CSMeanReversionHandler:
    return CSMeanReversionHandler(raw_data_client=raw_data_client)


def get_relative_carry_handler(
    carry_client: CarryClient = Depends(get_carry_repository),
) -> RelativeCarryHandler:
    return RelativeCarryHandler(carry_client=carry_client)


def get_relative_momentum_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> RelativeMomentumHandler:
    return RelativeMomentumHandler(raw_data_client=raw_data_client)
