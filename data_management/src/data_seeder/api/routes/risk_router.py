"""
This module defines an API route for seeding robust volatility data into the database.
It uses FastAPI for the API definitions and SQLAlchemy for the database interactions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.data_seeder.api.handlers.risk_handler import RiskHandler
from src.db.database import get_db

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/risk_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with Risk calculations",
)
async def seed_risk_data(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the risk table with data.
    """
    try:
        # Business logic is in a separate handler
        risk_handler = RiskHandler(db_session)
        await risk_handler.seed_calculate_risk_data_async()

        logger.info("Successfully seeded database with risk data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with raw data.",
        }

    except Exception as exception_error:
        logger.error("Failed to seed database with risk data: %s", exception_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from exception_error