# Standard Library
import logging

# Third-Party Libraries
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Application-specific imports
from src.handlers.seed_db_handler import SeedDBHandler
from src.database import get_db
from src.handlers.errors import DatabaseError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with Raw Data",
)
async def fill_database(db_session: AsyncSession = Depends(get_db)):
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
        ) from DatabaseError("Failed to seed database.")
