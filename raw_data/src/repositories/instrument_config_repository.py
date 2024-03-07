from sqlalchemy.ext.asyncio import AsyncSession
from src.models.config_models import InstrumentConfigModel
from src.schemas.config_schemas import InstrumentConfigSchema

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger

table_name = InstrumentConfigModel.__tablename__


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(
            db_session=db_session, schema=InstrumentConfigModel
        )
