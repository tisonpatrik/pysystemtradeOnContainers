"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from src.utils.logging import AppLogger

from src.db.api.database_route import router as database_router
from src.seed_raw_data.api.seed_raw_data_route import router as seed_db_router
from src.csv_io.api.csv_files_route import router as csv_files_router

logger = AppLogger.get_instance().get_logger()

app = FastAPI()

# app.include_router(router, prefix=settings.api_prefix)
app.include_router(database_router, prefix="/database")
app.include_router(csv_files_router, prefix="/csv_files_router")
app.include_router(seed_db_router, prefix="/raw_data_route")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
