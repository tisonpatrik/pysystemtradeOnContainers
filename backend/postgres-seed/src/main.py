"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from src.utils.logging import AppLogger

from src.db.api.database_route import router as database_router
from src.api.data_processing_route import router as parse_csv_files
from src.seed_raw_data.api.seed_raw_data_route import router as seed_db_router
from src.api.seed_risk_route import router as risk_router

logger = AppLogger.get_instance().get_logger()

app = FastAPI()

# app.include_router(router, prefix=settings.api_prefix)
app.include_router(database_router, prefix="/database")
app.include_router(parse_csv_files, prefix="/parse_csv_files")
app.include_router(seed_db_router, prefix="/raw_data_route")
app.include_router(risk_router, prefix="/seed_risk_route")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
