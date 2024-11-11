from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_client, get_db_repository
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.http_client.rest_client import RestClient
from positions.api.handlers.positions_handler import PositionsHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app):
        yield


async def get_positions_handler(
    db_repository: Repository = Depends(get_db_repository),
    client: RestClient = Depends(get_client),
) -> PositionsHandler:
    return PositionsHandler(repository=db_repository, client=client)
