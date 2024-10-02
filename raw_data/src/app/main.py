from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from common.src.middleware.middleware import AppMiddleware
from raw_data.src.api.dependencies.dependencies import app_lifespan
from raw_data.src.api.routers.daily_returns_vol_route import router as daily_returns_vol_route
from raw_data.src.api.routers.fx_prices_router import router as fx_prices_route
from raw_data.src.api.routers.raw_carry_router import router as raw_carry_route

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

app.include_router(fx_prices_route, prefix="/fx_prices_route")
app.include_router(raw_carry_route, prefix="/raw_carry_route")
app.include_router(daily_returns_vol_route, prefix="/daily_returns_vol_route")
