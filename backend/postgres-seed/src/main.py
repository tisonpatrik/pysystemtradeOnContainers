"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from src.config import settings
from src.utils.logging import AppLogger

from src.api.database_route import router as database_router
from src.api.data_processing_route import router as parse_csv_files
from src.api.seed_raw_data_route import router as seed_db_router
from src.api.seed_risk_route import router as risk_router

logger = AppLogger.get_instance().get_logger()

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

# app.include_router(router, prefix=settings.api_prefix)
app.include_router(database_router, prefix="/database")
app.include_router(parse_csv_files, prefix="/parse_csv_files")
app.include_router(seed_db_router, prefix="/seed_raw_data_route")
app.include_router(risk_router, prefix="/seed_risk_route")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
