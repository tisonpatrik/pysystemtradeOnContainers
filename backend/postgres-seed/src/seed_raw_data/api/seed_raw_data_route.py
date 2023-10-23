"""
API route definitions for seeding the database with raw data.
Handles all incoming HTTP requests related to this functionality.
"""

import logging

# Third-Party Libraries
from fastapi import APIRouter, HTTPException, status

# Application-specific imports
from src.seed_raw_data.handlers.seed_db_handler import SeedDBHandler

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
async def fill_database():
    """
    Fills the database tables with data.
    """
    try:
        # Business logic is in a separate handler
        seed_db_handler = SeedDBHandler()
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


@router.get(
    "/get_csv_file_counts/",
    status_code=status.HTTP_200_OK,
    name="Get Count of Mounted CSV Files",
)
async def get_csv_file_counts():
    """
    Returns the count of CSV files in specified directories.
    """
    try:
        seed_db_handler = SeedDBHandler()
        counts = await seed_db_handler.get_count_of_mounted_files_async()

        logger.info("Successfully counted CSV files: %s", counts)
        return {
            "status": "success",
            "message": "Successfully counted CSV files.",
            "counts": counts,
        }

    except Exception as e:
        logger.error("Failed to count CSV files: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while counting CSV files.",
        ) from e