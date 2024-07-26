from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from forecast.src.api.dependencies.forecast_dependencies import app_lifespan
from forecast.src.api.routers.raw_forecast_router import router as raw_forecast_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(raw_forecast_route, prefix="/get_raw_forecast_route")
logger = AppLogger.get_instance().get_logger()
