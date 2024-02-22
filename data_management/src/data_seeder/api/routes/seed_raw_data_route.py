"""
API route definitions for seeding the database with raw data.
Handles all incoming HTTP requests related to this functionality.
"""

# Third-Party Libraries
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.data_seeder.api.handlers.seed_config_data_handler import SeeConfigDataHandler
from src.data_seeder.api.handlers.seed_raw_data_handler import SeedRawDataHandler

from src.app.dependencies import get_db

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
        seed_db_handler = SeeConfigDataHandler(db_session)
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


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with Raw Data",
)
async def fill_database_async(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the database tables with data.
    """
    try:
        # Business logic is in a separate handler
        seed_db_handler = SeedRawDataHandler(db_session)
        await seed_db_handler.seed_data_from_csv_async()

        logger.info("Successfully seeded database with raw data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with raw data.",
        }

    except Exception as error:
        logger.error("Failed to seed database with raw data: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from error
