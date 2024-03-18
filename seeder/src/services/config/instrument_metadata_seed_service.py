import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.db.entities_repository import EntitiesRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentMetadata


class InstrumentMetadataSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = EntitiesRepository(db_session, InstrumentMetadata)

    async def seed_instrument_metadata_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {InstrumentMetadata.__tablename__} data: ")
        data = [InstrumentMetadata(**row.to_dict()) for _, row in raw_data.iterrows()]
        # await self.repository.insert_many_async(data)
