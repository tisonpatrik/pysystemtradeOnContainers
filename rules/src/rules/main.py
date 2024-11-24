from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.logging.logger import AppLogger
from common.middleware.logging import AppMiddleware
from rules.api.dependencies.dependencies import app_lifespan
from rules.api.routes.accel_route import router as accel_route
from rules.api.routes.assettrend_route import router as assettrend_route
from rules.api.routes.breakout_route import router as breakout_route
from rules.api.routes.carry_route import router as carry_route
from rules.api.routes.cs_mean_reversion_route import router as cs_mean_reversion_route
from rules.api.routes.momentum_route import router as momentum_route
from rules.api.routes.normalized_momentum_route import router as normalized_momentum_route
from rules.api.routes.relative_carry_route import router as relative_carry_route
from rules.api.routes.relative_momentum_route import router as relative_momentum_route
from rules.api.routes.skewabs_route import router as skewabs_route
from rules.api.routes.skewrel_route import router as skewrel_route

logger = AppLogger.get_instance().get_logger()

app_configs = {
    "title": "Rules API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)
app.add_middleware(AppMiddleware)

app.include_router(accel_route, prefix="/accel_route")
app.include_router(breakout_route, prefix="/breakout_route")
app.include_router(assettrend_route, prefix="/assettrend_route")
app.include_router(carry_route, prefix="/carry_route")
app.include_router(momentum_route, prefix="/momentum_route")
app.include_router(cs_mean_reversion_route, prefix="/cross_sectional_mean_reversion_route")
app.include_router(relative_carry_route, prefix="/relative_carry_route")
app.include_router(relative_momentum_route, prefix="/relative_momentum_route")
app.include_router(skewabs_route, prefix="/skewabs_route")
app.include_router(skewrel_route, prefix="/skewrel_route")
app.include_router(normalized_momentum_route, prefix="/normalized_momentum_route")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.exception("Request validation error: %s", exc.errors())
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.exception("HTTP error occurred: %s", exc.detail)
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server error: %s", str(exc))
    return ORJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"})
