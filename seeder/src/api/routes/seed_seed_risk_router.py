from fastapi import APIRouter, Depends, HTTPException, status
from src.api.handlers.seed_risk_data_handler import SeedRiskDataHandler
from src.dependencies.risk_dependencies import get_daily_returns_vol_seed_service
from src.services.risk.seed_daily_returns_vol_service import SeedDailyReturnsVolService
from src.services.risk.seed_instrument_vol_service import SeedInstrumentVolService

from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_raw_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with raw data files",
)
async def seed_risk_data_async(
    seed_daily_returns_vol_service: SeedDailyReturnsVolService = Depends(get_daily_returns_vol_seed_service),
):
    """
    Fills the database tables with data.
    """
    try:
        seed_db_handler = SeedRiskDataHandler(seed_daily_returns_vol_service)
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
