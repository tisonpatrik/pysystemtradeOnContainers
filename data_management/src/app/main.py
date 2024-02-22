"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from src.api.routes.seed_raw_data_route import router as seed_db_router
from src.api.routes.seed_risk_router import router as risk_router
from src.api.routes.seed_tradable_instruments_route import (
    router as tradable_instruments_router,
)
from common.logging.logging import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI()

app.include_router(seed_db_router, prefix="/seed_csv_data_route")
app.include_router(risk_router, prefix="/seed_risk_data_route")
app.include_router(
    tradable_instruments_router, prefix="/seed_tradable_instruments_route"
)


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
