from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.carry_client import CarryClient
from common.src.clients.prices_client import PricesClient
from common.src.clients.raw_data_client import RawDataClient
from common.src.dependencies.core_dependencies import (
    get_carry_client,
    get_daily_prices_client,
    get_raw_data_client,
    get_redis,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisRepository
from rules.api.handlers.accel_handler import AccelHandler
from rules.api.handlers.assettrend_handler import AssettrendHandler
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.breakout_handler import BreakoutHandler
from rules.api.handlers.carry_handler import CarryHandler
from rules.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler
from rules.api.handlers.momentum_handler import MomentumHandler
from rules.api.handlers.momentum_rule_handler import MomentumRuleHandler
from rules.api.handlers.relative_carry_handler import RelativeCarryHandler
from rules.api.handlers.relative_momentum_handler import RelativeMomentumHandler
from rules.api.handlers.skewabs_handler import SkewAbsHandler
from rules.api.handlers.skewrel_handler import SkewRelHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_attenuation_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> AttenutationHandler:
    return AttenutationHandler(raw_data_client=raw_data_client)


def get_momentum_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> MomentumHandler:
    return MomentumHandler(prices_client=prices_client, raw_data_client=raw_data_client, redis_repository=redis_repository)


def get_momentum_rule_handler(
    momentum_handler: MomentumHandler = Depends(get_momentum_handler),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> MomentumRuleHandler:
    return MomentumRuleHandler(momentum_handler=momentum_handler, attenuation_handler=attenuation_handler)


def get_accel_handler(
    momentum_handler: MomentumHandler = Depends(get_momentum_handler),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> AccelHandler:
    return AccelHandler(momentum_handler=momentum_handler, attenuation_handler=attenuation_handler)


def get_breakout_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> BreakoutHandler:
    return BreakoutHandler(prices_client=prices_client, attenuation_handler=attenuation_handler)


def get_asserttrend_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> AssettrendHandler:
    return AssettrendHandler(raw_data_client=raw_data_client, attenuation_handler=attenuation_handler)


def get_carry_handler(
    carry_client: CarryClient = Depends(get_carry_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> CarryHandler:
    return CarryHandler(carry_client=carry_client, attenuation_handler=attenuation_handler)


def get_cs_mean_reversion_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> CSMeanReversionHandler:
    return CSMeanReversionHandler(raw_data_client=raw_data_client, attenuation_handler=attenuation_handler)


def get_relative_carry_handler(
    carry_client: CarryClient = Depends(get_carry_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> RelativeCarryHandler:
    return RelativeCarryHandler(carry_client=carry_client, attenuation_handler=attenuation_handler)


def get_relative_momentum_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> RelativeMomentumHandler:
    return RelativeMomentumHandler(raw_data_client=raw_data_client, attenuation_handler=attenuation_handler)


def get_skewabs_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> SkewAbsHandler:
    return SkewAbsHandler(raw_data_client=raw_data_client, attenuation_handler=attenuation_handler)


def get_skewrel_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
    attenuation_handler: AttenutationHandler = Depends(get_attenuation_handler),
) -> SkewRelHandler:
    return SkewRelHandler(raw_data_client=raw_data_client, attenuation_handler=attenuation_handler)
