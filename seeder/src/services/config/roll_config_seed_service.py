import pandas as pd

from common.src.database.repository import Repository
from common.src.database.statements.insert_statement import InsertStatement
from common.src.logging.logger import AppLogger
from common.src.models.config_models import RollConfigModel


class RollConfigSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_roll_config_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding {RollConfigModel.__tablename__} data: ")
        statement = InsertStatement(table_name=RollConfigModel.__tablename__, data=raw_data)
        await self.repository.insert_dataframe_async(statement)
