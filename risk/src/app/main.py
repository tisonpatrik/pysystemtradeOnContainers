from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from common.src.middleware.middleware import AppMiddleware
from risk.src.api.dependencies.dependencies import app_lifespan
from risk.src.api.routers.daily_returns_vol_route import router as daily_returns_vol_route
from risk.src.api.routers.instrument_volatility_route import router as instrument_vol_route
from risk.src.api.routers.normalized_prices_for_asset_class_router import router as normalized_prices_for_asset_class_route

app_configs = {
    "title": "Risk API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)
app.add_middleware(AppMiddleware)

app.include_router(instrument_vol_route, prefix="/instrument_currency_vol_route")
app.include_router(daily_returns_vol_route, prefix="/daily_returns_vol_route")
app.include_router(normalized_prices_for_asset_class_route, prefix="/normalized_prices_for_asset_class_router")
