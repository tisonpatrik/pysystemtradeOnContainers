from asyncpg import Connection
from fastapi import Depends
from src.services.config.instrument_config_seed_service import \
    InstrumentConfigSeedService
from src.services.config.instrument_metadata_seed_service import \
    InstrumentMetadataSeedService
from src.services.config.roll_config_seed_service import RollConfigSeedService
from src.services.config.spread_cost_seed_service import SpreadCostSeedService

from common.src.database.dependencies import get_db


def get_seed_config_service(db_session: Connection = Depends(get_db)) -> InstrumentConfigSeedService:
    return InstrumentConfigSeedService(db_session)

def get_instrument_metadata_seed_service(db_session: Connection = Depends(get_db)) -> InstrumentMetadataSeedService:
    return InstrumentMetadataSeedService(db_session)

def get_roll_config_seed_service(db_session: Connection = Depends(get_db)) -> RollConfigSeedService:
    return RollConfigSeedService(db_session)

def get_spread_cost_seed_service(db_session: Connection = Depends(get_db)) -> SpreadCostSeedService:
    return SpreadCostSeedService(db_session)