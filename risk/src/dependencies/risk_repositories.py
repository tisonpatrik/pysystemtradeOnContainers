from asyncpg import Connection
from fastapi import Depends

from common.src.database.base_model import BaseModel
from common.src.database.repository import Repository
from common.src.dependencies.db_dependencies import get_db
from risk.src.models.risk_models import DailyReturnsVolatility


def get_daily_returns_vol_repository(db_session: Connection = Depends(get_db)) -> Repository[BaseModel]:
    return Repository(db_session, DailyReturnsVolatility)
