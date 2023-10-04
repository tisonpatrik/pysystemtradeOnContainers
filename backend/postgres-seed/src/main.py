"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from src.config import settings
from src.utils.logging import AppLogger

from src.api.config_files_route import router as config_files_router
from src.api.database_route import router as database_router
from src.api.raw_data_route import router as raw_data_router
from src.api.seed_db_route import router as seed_db_router
from src.api.risk_route import router as risk_router

logger = AppLogger.__call__().get_logger()

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
app.include_router(config_files_router, prefix="/config_files")
app.include_router(raw_data_router, prefix="/raw_data")
app.include_router(seed_db_router, prefix="/seed_db")
app.include_router(risk_router, prefix="/risk")

@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
