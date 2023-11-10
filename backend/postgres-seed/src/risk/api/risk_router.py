"""
This module defines an API route for seeding robust volatility data into the database.
It uses FastAPI for the API definitions and SQLAlchemy for the database interactions.
"""

import logging

# Third-Party Libraries
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.settings.database import get_db
from src.risk.handlers.robust_volatility_handler import RobustVolatilityHandler
from src.risk.handlers.instrument_volatility_handler import InstrumentVolatilityHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/robust_volatility_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Robust volatility data into db",
)
async def seed_robust_volatility_data(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the robust volatility table with data.
    """
    try:
        # Business logic is in a separate handler
        seed_db_handler = RobustVolatilityHandler(db_session)
        await seed_db_handler.insert_robust_volatility_async()

        logger.info("Successfully seeded database with risk data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with risk data.",
        }

    except Exception as exception_error:
        logger.error("Failed to seed database with raw data: %s", exception_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from exception_error


@router.post(
    "/instrument_volatility_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Instrument volatility data into db",
)
async def seed_instrument_volatility_data(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the instrument volatility table with data.
    """
    try:
        # Business logic is in a separate handler
        seed_db_handler = InstrumentVolatilityHandler(db_session)
        await seed_db_handler.insert_robust_volatility_async()

        logger.info("Successfully seeded database with risk data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with risk data.",
        }

    except Exception as exception_error:
        logger.error("Failed to seed database with raw data: %s", exception_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from exception_error
