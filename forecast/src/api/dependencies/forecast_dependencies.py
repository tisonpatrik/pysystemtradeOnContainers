from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from forecast.src.api.handlers.raw_forecast_handler import RawForecastHandler


async def get_raw_forecast_handler(
    db_repository: Repository = Depends(get_repository),
) -> RawForecastHandler:
    return RawForecastHandler(db_repository=db_repository)
