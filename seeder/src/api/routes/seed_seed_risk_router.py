from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status

# from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.seed_risk_data_handler import SeedRiskDataHandler

# from common.src.database.dependencies import get_db
from common.src.db.dependencies import get_db
from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with raw data files",
)
async def seed_risk_data_async(db_session: AsyncGenerator = Depends(get_db)):
    """
    Fills the database tables with data.
    """
    try:
        seed_db_handler = SeedRiskDataHandler(db_session)
        await seed_db_handler.seed_calculate_risk_data_async()

        logger.info("Successfully seeded database with risk data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with risk data.",
        }

    except Exception as error:
        logger.error("Failed to seed database with risk data: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding risk data to database.",
        ) from error
