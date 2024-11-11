from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from common.src.middleware.logging import AppMiddleware
from forecast.api.dependencies.forecast_dependencies import app_lifespan
from forecast.api.routers.raw_forecast_router import router as raw_forecast_route

app_configs = {
    "title": "RawData API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)
app.add_middleware(AppMiddleware)

app.include_router(raw_forecast_route, prefix="/get_raw_forecast_route")
