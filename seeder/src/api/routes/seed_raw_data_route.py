from fastapi import APIRouter, Depends, HTTPException, status
from src.api.handlers.seed_raw_data_handler import SeedRawDataHandler
from src.dependencies.raw_data_dependencies import (
    get_seed_adjusted_prices_service,
    get_seed_fx_prices_service,
    get_seed_multiple_prices_service,
    get_seed_roll_calendars_service,
)
from src.services.raw_data.seed_adjusted_prices_service import SeedAdjustedPricesService
from src.services.raw_data.seed_fx_prices_service import SeedFxPricesService
from src.services.raw_data.seed_multiple_prices_service import SeedMultiplePricesService
from src.services.raw_data.seed_roll_calendars_service import SeedRollCalendarsService

from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with raw data files",
)
async def seed_raw_data_files_route_async(
    seed_adjusted_prices_service: SeedAdjustedPricesService = Depends(get_seed_adjusted_prices_service),
    seed_fx_prices_service: SeedFxPricesService = Depends(get_seed_fx_prices_service),
    seed_multiple_prices_service: SeedMultiplePricesService = Depends(get_seed_multiple_prices_service),
    seed_roll_calendars_service: SeedRollCalendarsService = Depends(get_seed_roll_calendars_service),
):
    """
    Fills the database tables with data.
    """
    try:
        seed_db_handler = SeedRawDataHandler(
            seed_adjusted_prices_service,
            seed_fx_prices_service,
            seed_multiple_prices_service,
            seed_roll_calendars_service,
        )
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
