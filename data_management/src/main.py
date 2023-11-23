"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.core.utils.logging import AppLogger
from src.raw_data.api.routes.seed_raw_data_route import router as seed_db_router
from src.risk.api.routes.risk_router import router as risk_router

logger = AppLogger.get_instance().get_logger()

app = FastAPI()

app.include_router(seed_db_router, prefix="/raw_data_route")
app.include_router(risk_router, prefix="/risk_data_route")


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
