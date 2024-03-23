from asyncpg import Connection
from fastapi import Depends

from common.src.database.base_model import BaseModel
from common.src.dependencies.db_dependencies import get_db
from common.src.database.repository import Repository
from raw_data.src.models.config_models import InstrumentMetadataModel, RollConfigModel, SpreadCostsModel
from raw_data.src.models.instrument_config_models import InstrumentConfigModel
from raw_data.src.models.raw_data_models import (
    AdjustedPricesModel,
    FxPricesModel,
    MultiplePricesModel,
    RollCalendarsModel,
)


def get_instrument_config_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, InstrumentConfigModel)


def get_instrument_metadata_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, InstrumentMetadataModel)


def get_roll_config_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, RollConfigModel)


def get_spread_cost_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, SpreadCostsModel)


def get_adjusted_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, AdjustedPricesModel)


def get_fx_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, FxPricesModel)


def get_multiple_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, MultiplePricesModel)


def get_roll_calendars_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, RollCalendarsModel)
