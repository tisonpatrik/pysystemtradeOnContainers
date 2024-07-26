from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from common.src.dependencies.db_setup import setup_async_database
from forecast.src.api.handlers.raw_forecast_handler import RawForecastHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield


async def get_raw_forecast_handler(
    db_repository: Repository = Depends(get_repository),
) -> RawForecastHandler:
    return RawForecastHandler(db_repository=db_repository)
