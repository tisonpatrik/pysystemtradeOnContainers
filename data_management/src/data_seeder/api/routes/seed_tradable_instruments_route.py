from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.data_seeder.api.handlers.seed_tradable_instruments_handler import (
    SeedTradableInstrumentsHandler,
)
from src.db.database import get_db

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_tradable_instruments_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with Raw Data",
)
async def fill_database_async(db_session: AsyncSession = Depends(get_db)):
    """
    Fills the database tables with data.
    """
    try:
        # Business logic is in a separate handler
        seed_handler = SeedTradableInstrumentsHandler(db_session)
        await seed_handler.seed_tradable_instruments_async()

        logger.info("Successfully seeded database with tradable instruments data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with tradable instruments data.",
        }

    except Exception as error:
        logger.error(
            "Failed to seed database with tradable instruments data: %s", error
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from error
