"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from seeder.src.api.dependencies.app_dependencies import app_lifespan
from seeder.src.api.routes.seed_config_files_route import router as seed_config_router
from seeder.src.api.routes.seed_raw_data_route import router as seed_raw_data_router

logger = AppLogger.get_instance().get_logger()

app = FastAPI(lifespan=app_lifespan)

app.include_router(seed_config_router, prefix="/seed_config_router")
app.include_router(seed_raw_data_router, prefix="/seed_raw_data_router")
