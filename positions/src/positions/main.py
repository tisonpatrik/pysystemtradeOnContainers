from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from common.src.middleware.logging import AppMiddleware
from positions.api.dependencies.positions_dependencies import app_lifespan
from positions.api.routers.positions_route import router as position_route

app_configs = {
    "title": "Positions API",
    "description": "Service to provide rules for trading strategies.",
    "version": "0.1.0",
    "redirect_slashes": False,
    "lifespan": app_lifespan,
    "default_response_class": ORJSONResponse,
}

app = FastAPI(**app_configs)
app.add_middleware(AppMiddleware)

app.include_router(position_route, prefix="/position_route")
