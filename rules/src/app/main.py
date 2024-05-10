from fastapi import FastAPI

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger
from rules.src.api.routes.rules_router import router as rules_route

app = FastAPI(lifespan=app_lifespan)

app.include_router(rules_route, prefix='/rules_route')
logger = AppLogger.get_instance().get_logger()
