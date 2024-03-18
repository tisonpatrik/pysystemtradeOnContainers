import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.db.repository import Repository
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
        data = list(map(lambda row: RollConfig(**row[1].to_dict()), raw_data.iterrows()))
        await self.repository.insert_data_async(data)