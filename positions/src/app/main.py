from fastapi import FastAPI

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger
from positions.src.api.routers.positions_route import router as position_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(position_route, prefix="/position_route")
logger = AppLogger.get_instance().get_logger()
