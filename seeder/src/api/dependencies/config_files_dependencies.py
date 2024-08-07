from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_db_repository
from seeder.src.services.config.instrument_config_seed_service import InstrumentConfigSeedService
from seeder.src.services.config.instrument_metadata_seed_service import InstrumentMetadataSeedService
from seeder.src.services.config.roll_config_seed_service import RollConfigSeedService
from seeder.src.services.config.spread_cost_seed_service import SpreadCostSeedService


def get_seed_config_service(
	repository: Repository = Depends(get_db_repository),
) -> InstrumentConfigSeedService:
	return InstrumentConfigSeedService(repository)


def get_instrument_metadata_seed_service(
	repository: Repository = Depends(get_db_repository),
) -> InstrumentMetadataSeedService:
	return InstrumentMetadataSeedService(repository)


def get_roll_config_seed_service(
	repository: Repository = Depends(get_db_repository),
) -> RollConfigSeedService:
	return RollConfigSeedService(repository)


def get_spread_cost_seed_service(repository: Repository = Depends(get_db_repository)) -> SpreadCostSeedService:
	return SpreadCostSeedService(repository)
