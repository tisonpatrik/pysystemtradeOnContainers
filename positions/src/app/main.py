from fastapi import FastAPI

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger
from positions.src.api.routers.positions_route import router as run_simulation_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(run_simulation_route, prefix="/run_simulation_route")
logger = AppLogger.get_instance().get_logger()
