"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.api.routes.seed_risk_router import router as risk_router

from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI()

app.include_router(risk_router, prefix="/seed_risk_data_route")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
