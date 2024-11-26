from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.logging.logger import AppLogger
from common.middleware.logging import AppMiddleware
from positions.api.dependencies.dependencies import app_lifespan
from positions.api.routers.positions_route import router as position_route

logger = AppLogger.get_instance().get_logger()

app_configs = {
    "title": "Positions API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)  # type: ignore
app.add_middleware(AppMiddleware)

app.include_router(position_route, prefix="/position_route")


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
