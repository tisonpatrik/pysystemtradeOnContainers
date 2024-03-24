from asyncpg import Connection
from fastapi import Depends

from common.src.database.base_model import BaseModel
from common.src.database.repository import Repository
from common.src.database.statement_factory import StatementFactory
from common.src.dependencies.db_dependencies import get_db
from raw_data.src.models.raw_data_models import (
    AdjustedPricesModel,
    FxPricesModel,
    MultiplePricesModel,
    RollCalendarsModel,
)


def get_adjusted_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, AdjustedPricesModel)


def get_daily_prices_statement_factory(db_session: Connection = Depends(get_db)) -> StatementFactory:
    return StatementFactory(db_session, BaseModel)


def get_fx_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, FxPricesModel)


def get_multiple_prices_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, MultiplePricesModel)


def get_roll_calendars_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, RollCalendarsModel)
