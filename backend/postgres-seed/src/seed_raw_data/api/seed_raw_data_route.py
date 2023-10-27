"""
API route definitions for seeding the database with raw data.
Handles all incoming HTTP requests related to this functionality.
"""

import logging

# Third-Party Libraries
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.settings.database import get_db
from src.seed_raw_data.handlers.seed_db_handler import SeedDBHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()


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
        seed_db_handler = SeedDBHandler(db_session)
        await seed_db_handler.insert_data_from_csv_async()

        logger.info("Successfully seeded database with raw data.")
        return {
            "status": "success",
            "message": "Database successfully seeded with raw data.",
        }

    except Exception as e:
        logger.error("Failed to seed database with raw data: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while seeding the database.",
        ) from e
