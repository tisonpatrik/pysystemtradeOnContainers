from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import app_lifespan
from raw_data.src.api.routes.fx_prices_router import router as fx_prices_route
from raw_data.src.api.routes.normalized_prices_for_asset_class_router import router as normalized_prices_for_asset_class_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(fx_prices_route, prefix="/fx_prices_route")
app.include_router(normalized_prices_for_asset_class_route, prefix="/normalized_prices_for_asset_class_router")
logger = AppLogger.get_instance().get_logger()
