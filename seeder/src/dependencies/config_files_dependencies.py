from fastapi import Depends, Request
from src.services.config.instrument_config_seed_service import InstrumentConfigSeedService
from src.services.config.instrument_metadata_seed_service import InstrumentMetadataSeedService
from src.services.config.roll_config_seed_service import RollConfigSeedService
from src.services.config.spread_cost_seed_service import SpreadCostSeedService

from common.src.database.repository import Repository


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_seed_config_service(
    repository: Repository = Depends(get_repository),
) -> InstrumentConfigSeedService:
    return InstrumentConfigSeedService(repository)


def get_instrument_metadata_seed_service(
    repository: Repository = Depends(get_repository),
) -> InstrumentMetadataSeedService:
    return InstrumentMetadataSeedService(repository)


def get_roll_config_seed_service(
    repository: Repository = Depends(get_repository),
) -> RollConfigSeedService:
    return RollConfigSeedService(repository)


def get_spread_cost_seed_service(repository: Repository = Depends(get_repository)) -> SpreadCostSeedService:
    return SpreadCostSeedService(repository)
