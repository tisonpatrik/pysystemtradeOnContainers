from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.seed_raw_data_handler import SeedRawDataHandler

from common.src.database.dependencies import get_db
from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with raw data files",
)
async def seed_raw_data_files_async(db_session: AsyncSession = Depends(get_db)):
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
            detail="An error occurred while seeding raw data to database.",
        ) from error
