"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.api.routes.test_route import router as test_router

from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI()
app.include_router(test_router, prefix="/test_router")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
