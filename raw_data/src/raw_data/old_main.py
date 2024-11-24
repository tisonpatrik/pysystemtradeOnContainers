from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.src.logging.logger import AppLogger
from common.src.middleware.logging import AppMiddleware
from raw_data.old_api.dependencies.dependencies import app_lifespan
from raw_data.old_api.routers.cumulative_daily_vol_normalised_returns_router import (
    router as cumulative_daily_vol_normalised_returns_route,
)
from raw_data.old_api.routers.daily_returns_vol_route import router as daily_returns_vol_route
from raw_data.old_api.routers.fx_prices_router import router as fx_prices_route
from raw_data.old_api.routers.instrument_volatility_route import router as instrument_vol_route
from raw_data.old_api.routers.median_carry_for_asset_class_route import router as median_carry_for_asset_class_route
from raw_data.old_api.routers.normalized_prices_for_asset_class_router import (
    router as normalized_prices_for_asset_class_route,
)
from raw_data.old_api.routers.raw_carry_router import router as raw_carry_route
from raw_data.old_api.routers.relative_skew_deviation_router import router as relative_skew_deviation_route
from raw_data.old_api.routers.smooth_carry_router import router as smooth_carry_route
from raw_data.old_api.routers.vol_attenuation_router import router as vol_attenuation_route

logger = AppLogger.get_instance().get_logger()

app_configs = {
    "title": "Raw data API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)
app.add_middleware(AppMiddleware)

app.include_router(instrument_vol_route, prefix="/instrument_currency_vol_route")
app.include_router(normalized_prices_for_asset_class_route, prefix="/normalized_prices_for_asset_class_route")
app.include_router(cumulative_daily_vol_normalised_returns_route, prefix="/cumulative_daily_vol_normalised_returns_route")
app.include_router(fx_prices_route, prefix="/fx_prices_route")
app.include_router(raw_carry_route, prefix="/raw_carry_route")
app.include_router(daily_returns_vol_route, prefix="/daily_returns_vol_route")
app.include_router(smooth_carry_route, prefix="/smooth_carry_route")
app.include_router(median_carry_for_asset_class_route, prefix="/median_carry_for_asset_class_route")
app.include_router(relative_skew_deviation_route, prefix="/relative_skew_deviation_route")
app.include_router(vol_attenuation_route, prefix="/vol_attenuation_route")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    logger.exception("Request validation error: %s", exc.errors())
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException) -> ORJSONResponse:
    logger.exception("HTTP error occurred: %s", exc.detail)
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    logger.exception("Unhandled server error: %s", str(exc))
    return ORJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"})
