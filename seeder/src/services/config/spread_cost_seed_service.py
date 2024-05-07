import pandas as pd

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.queries.insert_statement import InsertStatement


class SpreadCostSeedService:
    """
    Service for seeding instrument config data.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_spread_costs_async(self, raw_data: pd.DataFrame):
        """
        Seed instrument config data.
        """
        self.logger.info(f"Seeding spred_costs data: ")
        statement = InsertStatement(table_name="spred_costs", data=raw_data)
        await self.repository.insert_dataframe_async(statement)
