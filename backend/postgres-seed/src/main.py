"""Main FastAPI application setup and configuration."""

import logging

from fastapi import FastAPI

from src.api.router import router
from src.core.config import settings
from src.db.database import Database

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)
db = Database(settings.database_url)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """A simple ping endpoint for checking the API's status."""
    return {"Ping": "Pong!"}

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.close()