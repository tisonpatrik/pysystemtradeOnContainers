import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import SpreadCosts


class SpreadCostSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, SpreadCosts)

    async def seed_spread_costs_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {SpreadCosts.__tablename__} data: ")
        await self.repository.insert_dataframe_async(raw_data)
