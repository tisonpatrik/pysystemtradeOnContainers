import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import RollConfig


class RollConfigSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, RollConfig)

    async def seed_roll_config_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {RollConfig.__tablename__} data: ")
        data = [RollConfig(**row.to_dict()) for _, row in raw_data.iterrows()]
        await self.repository.insert_many_async(data)
