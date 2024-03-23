import pandas as pd

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.instrument_config_models import InstrumentConfigModel


class InstrumentConfigSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, repository: Repository[InstrumentConfigModel]):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_instrument_config_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {InstrumentConfigModel.__tablename__} data: ")
        await self.repository.insert_dataframe_async(raw_data)
