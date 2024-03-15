import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.entity_repository import EntityRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentConfig


class InstrumentConfigSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = EntityRepository(db_session, InstrumentConfig)

    async def seed_instrument_config_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {InstrumentConfig.__tablename__} data: ")
        data = [InstrumentConfig(**row.to_dict()) for _, row in raw_data.iterrows()]
        await self.repository.insert_many_async(data)
