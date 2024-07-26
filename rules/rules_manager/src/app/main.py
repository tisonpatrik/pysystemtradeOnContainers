from fastapi import FastAPI
from rules_manager.src.api.dependencies.rules_manager_dependencies import app_lifespan
from rules_manager.src.api.routes.rules_router import router as rules_route

from common.src.logging.logger import AppLogger

app = FastAPI(lifespan=app_lifespan)

app.include_router(rules_route, prefix="/rules_route")
logger = AppLogger.get_instance().get_logger()
