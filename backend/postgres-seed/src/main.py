"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from src.api.router import router
from src.config import settings
from src.utils.logging import AppLogger

logger = AppLogger.__call__().get_logger()

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
