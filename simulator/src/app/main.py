from fastapi import FastAPI

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger

app = FastAPI(lifespan=app_lifespan)

logger = AppLogger.get_instance().get_logger()
