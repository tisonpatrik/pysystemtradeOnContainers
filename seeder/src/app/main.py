"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.api.routes.seed_config_files_route import router as seed_config_router
from src.api.routes.seed_raw_data_route import router as seed_raw_data_router

from common.src.dependencies.app_dependencies import app_lifespan
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI(lifespan=app_lifespan)

app.include_router(seed_config_router, prefix="/seed_config_router")
app.include_router(seed_raw_data_router, prefix="/seed_raw_data_router")
