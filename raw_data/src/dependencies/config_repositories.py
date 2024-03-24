from asyncpg import Connection
from fastapi import Depends

from common.src.database.base_model import BaseModel
from common.src.database.repository import Repository
from common.src.database.statement_factory import StatementFactory
from common.src.dependencies.db_dependencies import get_db
from raw_data.src.models.config_models import InstrumentMetadataModel, RollConfigModel, SpreadCostsModel
from raw_data.src.models.instrument_config_models import InstrumentConfigModel


def get_instrument_config_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, InstrumentConfigModel)


def get_instrument_config_statement_factory(db_session: Connection = Depends(get_db)) -> StatementFactory[BaseModel]:
    return StatementFactory(db_session, InstrumentConfigModel)


def get_instrument_metadata_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, InstrumentMetadataModel)


def get_roll_config_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, RollConfigModel)


def get_spread_cost_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, SpreadCostsModel)
