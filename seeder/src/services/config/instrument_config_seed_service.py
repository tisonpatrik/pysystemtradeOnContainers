import pandas as pd

from common.src.database.base_statements.insert_statement import InsertManyStatement
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger


class InstrumentConfigSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_instrument_config_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info("Seeding instrument_config data: ")
        statement = InsertManyStatement(table_name="instrument_config", data=raw_data)
        await self.repository.insert_dataframe_async(statement)
