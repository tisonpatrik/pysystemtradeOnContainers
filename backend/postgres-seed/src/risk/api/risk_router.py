"""
bla
"""

import logging

# Third-Party Libraries
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.settings.database import get_db
from src.risk.handlers.robust_volatility_handler import RobustVolatilityHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/risk_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Robust volatility data into db",
)
async def seed_risk_data(db_session: AsyncSession = Depends(get_db)):
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

    except Exception as e:
        logger.error("Failed to seed database with raw data: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from e
