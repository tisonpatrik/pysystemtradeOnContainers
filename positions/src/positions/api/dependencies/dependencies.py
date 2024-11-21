from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.old_dependencies import get_forecast_client, get_raw_data_client
from common.src.clients.forecast_client import ForecastClient
from common.src.clients.raw_data_client import RawDataClient
from common.src.database.old_postgres_setup import setup_async_database
from common.src.http_client.old_rest_client_setup import setup_async_client
from common.src.redis.old_redis_setup import setup_async_redis
from positions.api.handlers.average_position_at_subsystem_level_handler import AveragePositionAtSubsystemLevelHandler
from positions.api.handlers.instrument_value_vol_handler import InstrumentValueVolHandler
from positions.api.handlers.positions_handler import PositionsHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app), setup_async_redis(app):
        yield


def get_instrument_value_vol_handler(raw_data_client: RawDataClient = Depends(get_raw_data_client)) -> InstrumentValueVolHandler:
    return InstrumentValueVolHandler(raw_data_client=raw_data_client)


def get_average_position_at_subsystem_level_handler(
    instrument_value_vol_handler: InstrumentValueVolHandler = Depends(get_instrument_value_vol_handler),
) -> AveragePositionAtSubsystemLevelHandler:
    return AveragePositionAtSubsystemLevelHandler(instrument_value_vol_handler=instrument_value_vol_handler)


def get_positions_handler(
    average_position_at_subsystem_level_handler: AveragePositionAtSubsystemLevelHandler = Depends(
        get_average_position_at_subsystem_level_handler
    ),
    forecast_client: ForecastClient = Depends(get_forecast_client),
) -> PositionsHandler:
    return PositionsHandler(
        average_position_at_subsystem_level_handler=average_position_at_subsystem_level_handler, forecast_client=forecast_client
    )
