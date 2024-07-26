from fastapi import APIRouter, Depends, HTTPException, status

from common.src.logging.logger import AppLogger
from seeder.src.api.dependencies.config_files_dependencies import (
    get_instrument_metadata_seed_service,
    get_roll_config_seed_service,
    get_seed_config_service,
    get_spread_cost_seed_service,
)
from seeder.src.api.handlers.seed_config_data_handler import SeedConfigDataHandler
from seeder.src.services.config.instrument_config_seed_service import InstrumentConfigSeedService
from seeder.src.services.config.instrument_metadata_seed_service import InstrumentMetadataSeedService
from seeder.src.services.config.roll_config_seed_service import RollConfigSeedService
from seeder.src.services.config.spread_cost_seed_service import SpreadCostSeedService

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/seed_config_data_route/",
    status_code=status.HTTP_201_CREATED,
    name="Seed Database with config data files",
)
async def seed_config_files_routes_async(
    config_seed_service: InstrumentConfigSeedService = Depends(get_seed_config_service),
    metadata_seed_service: InstrumentMetadataSeedService = Depends(get_instrument_metadata_seed_service),
    roll_config_seed_service: RollConfigSeedService = Depends(get_roll_config_seed_service),
    spread_cost_seed_service: SpreadCostSeedService = Depends(get_spread_cost_seed_service),
):
    """
    Fills the database tables with data.
    """
    try:
        seed_db_handler = SeedConfigDataHandler(
            config_seed_service,
            metadata_seed_service,
            roll_config_seed_service,
            spread_cost_seed_service,
        )
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
