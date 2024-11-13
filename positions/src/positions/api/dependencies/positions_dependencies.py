from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.raw_data_client import RawDataClient
from common.src.dependencies.core_dependencies import (
    get_raw_data_client,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from positions.api.handlers.positions_handler import PositionsHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


async def get_positions_handler(
    raw_data_client: RawDataClient = Depends(get_raw_data_client),
) -> PositionsHandler:
    return PositionsHandler(raw_data_client=raw_data_client)
