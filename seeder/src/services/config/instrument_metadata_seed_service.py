import pandas as pd

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentMetadataModel


class InstrumentMetadataSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_instrument_metadata_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {InstrumentMetadataModel.__tablename__} data: ")
        await self.repository.insert_dataframe_async(raw_data)
