from fastapi import FastAPI

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger
from raw_data.src.api.routes.fx_prices_router import router as fx_prices_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(fx_prices_route, prefix="/fx_prices_route")
logger = AppLogger.get_instance().get_logger()
