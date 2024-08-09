from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_db_repository,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app):
        yield


def get_fx_prices_handler(repository: Repository = Depends(get_db_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)
