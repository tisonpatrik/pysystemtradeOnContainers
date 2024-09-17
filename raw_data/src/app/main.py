from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import app_lifespan
from raw_data.src.api.routers.daily_annualised_roll_router import router as daily_annualised_roll_route
from raw_data.src.api.routers.fx_prices_router import router as fx_prices_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(fx_prices_route, prefix="/fx_prices_route")
app.include_router(daily_annualised_roll_route, prefix="/daily_annualised_roll_route")
logger = AppLogger.get_instance().get_logger()
