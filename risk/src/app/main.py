from fastapi import FastAPI

from risk.src.api.dependencies.risk_dependencies import app_lifespan
from common.src.logging.logger import AppLogger
from risk.src.api.routers.instrument_volatility_route import router as instrument_vol_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(instrument_vol_route, prefix="/instrument_currency_vol_route")
logger = AppLogger.get_instance().get_logger()
