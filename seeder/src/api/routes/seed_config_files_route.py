"""
API route definitions for seeding the database with raw data.
Handles all incoming HTTP requests related to this functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.dependencies import get_db
from common.src.logging.logger import AppLogger
from seeder.src.api.handlers.seed_config_data_handler import SeedConfigDataHandler

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


@router.get(
    "/test_route/",
    status_code=status.HTTP_200_OK,
)
async def get_instrument_config_count():
    """
    Retrieves the count of instrument config items.
    """
    try:
        async with AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/test_router/get_count_of_instrument_config_items/"
            )
            if response.status_code == 200:
                count = response.json()["count"]
                logger.info(
                    f"Successfully retrieved count of instrument config items: {count}"
                )
                return {
                    "status": "success",
                    "count": count,
                }
            else:
                logger.error(
                    f"Failed to retrieve count, status code: {response.status_code}"
                )
                return {
                    "status": "error",
                    "message": "Failed to retrieve count of instrument config items.",
                }

    except Exception as error:
        logger.error(
            "Failed to retrieve count of instrument config items: %s", str(error)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving count of instrument config items.",
        ) from error
