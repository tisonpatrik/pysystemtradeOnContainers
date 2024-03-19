"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI

from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
