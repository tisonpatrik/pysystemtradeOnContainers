import pandas as pd

from common.src.database.repository import Repository
from common.src.queries.insert_statement import InsertStatement
from common.src.logging.logger import AppLogger


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
        self.logger.info(f"Seeding instrument_metadata data: ")
        statement = InsertStatement(table_name="instrument_metadata", data=raw_data)
        await self.repository.insert_dataframe_async(statement)
