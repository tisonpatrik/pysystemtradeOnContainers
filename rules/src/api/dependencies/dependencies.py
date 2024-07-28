from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_client, get_repository
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.http_client.rest_client import RestClient
from rules.src.api.handlers.accel_handler import AccelHandler
from rules.src.api.handlers.assettrend_handler import AssettrendHandler
from rules.src.api.handlers.breakout_handler import BreakoutHandler
from rules.src.api.handlers.rules_manager_handler import RulesManagerHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app):
        yield


def get_rules_handler(repository: Repository = Depends(get_repository)) -> RulesManagerHandler:
    return RulesManagerHandler(repository=repository)


def get_accel_handler(
    repository: Repository = Depends(get_repository),
    client: RestClient = Depends(get_client),
) -> AccelHandler:
    return AccelHandler(repository=repository, client=client)


def get_breakout_handler(
    repository: Repository = Depends(get_repository),
    client: RestClient = Depends(get_client),
) -> BreakoutHandler:
    return BreakoutHandler(repository=repository, client=client)


def get_asserttrend_handler(
    repository: Repository = Depends(get_repository),
    client: RestClient = Depends(get_client),
) -> AssettrendHandler:
    return AssettrendHandler(repository=repository, client=client)
