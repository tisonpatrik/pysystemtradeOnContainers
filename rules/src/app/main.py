from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from common.src.middleware.middleware import AppMiddleware
from rules.src.api.dependencies.dependencies import app_lifespan
from rules.src.api.routes.accel_route import router as accel_route
from rules.src.api.routes.assettrend_route import router as assettrend_route
from rules.src.api.routes.breakout_route import router as breakout_route
from rules.src.api.routes.carry_route import router as carry_route
from rules.src.api.routes.cs_mean_reversion_route import router as cd_mean_reversion_route
from rules.src.api.routes.momentum_route import router as momentum_route
from rules.src.api.routes.relative_carry_route import router as relative_carry_route
from rules.src.api.routes.relative_momentum_route import router as relative_momentum_route
from rules.src.api.routes.rules_manager_router import router as rules_manager_route

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

app.include_router(rules_manager_route, prefix="/rules_manager_route")
app.include_router(accel_route, prefix="/accel_route")
app.include_router(breakout_route, prefix="/breakout_route")
app.include_router(assettrend_route, prefix="/assettrend_route")
app.include_router(carry_route, prefix="/carry_route")
app.include_router(momentum_route, prefix="/momentum_route")
app.include_router(cd_mean_reversion_route, prefix="/cd_mean_reversion_route")
app.include_router(relative_carry_route, prefix="/relative_carry_route")
app.include_router(relative_momentum_route, prefix="/relative_momentum_route")
