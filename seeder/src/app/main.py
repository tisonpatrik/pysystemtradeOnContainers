"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.api.routes.seed_config_files_route import router as seed_config_router
from src.api.routes.seed_raw_data_route import router as seed_raw_data_router
from src.api.routes.seed_seed_risk_router import router as risk_router

from common.src.dependencies.database_dependencies import get_db
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI(lifespan=get_db)

app.include_router(seed_config_router, prefix="/seed_config_router")
app.include_router(seed_raw_data_router, prefix="/seed_raw_data_router")
app.include_router(risk_router, prefix="/seed_risk_data_route")
