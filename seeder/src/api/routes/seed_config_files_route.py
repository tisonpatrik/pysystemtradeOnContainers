"""
API route definitions for seeding the database with raw data.
Handles all incoming HTTP requests related to this functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.seed_config_data_handler import SeedConfigDataHandler

from common.src.database.dependencies import get_db
from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_config_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with config data files",
)
async def seed_config_files_async(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the database tables with data.
    """
    try:
        # Business logic is in a separate handler
        seed_db_handler = SeedConfigDataHandler(db_session)
        await seed_db_handler.seed_data_from_csv_async()

        logger.info("Successfully seeded database with config data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with config data.",
        }

    except Exception as error:
        logger.error("Failed to seed database with config data: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding config data to database.",
        ) from error
