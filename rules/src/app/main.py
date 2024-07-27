from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from rules.src.api.dependencies.rules_manager_dependencies import app_lifespan
from rules.src.api.routes.rules_manager_router import router as rules_manager_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(rules_manager_route, prefix="/rules_manager_route")
logger = AppLogger.get_instance().get_logger()
