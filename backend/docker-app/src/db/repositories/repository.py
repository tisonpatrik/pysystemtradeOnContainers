from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper
from src.core.config import settings

import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PostgresRepository:
    def __init__(self):
        self.database_url: str = settings.sync_database_url
        self.inserter = DataInserter(self.database_url)
        self.loader = DataLoader(self.database_url)
        self.creator = TableCreator(self.database_url)
        self.dropper = TableDropper(self.database_url)

    async def insert_data_async(self, df: pd.DataFrame, table_name: str) -> None:
        """Inserts data from a DataFrame into a specified table asynchronously."""
        try:
            await self.inserter.insert_dataframe_async(df, table_name)
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            raise

    async def load_data_async(self, sql_template: str, parameters: dict = None) -> pd.DataFrame:
        """Loads data asynchronously based on the provided SQL template and parameters."""
        try:
            return await self.loader.fetch_data_as_dataframe_async(sql_template, parameters)
        except Exception as e:
            logger.error(f"Error loading data with SQL template {sql_template}: {e}")
            raise

    def create_table(self, sql_command: str) -> None:
        """Creates a table using the provided SQL command."""
        try:
            self.creator.create_table(sql_command=sql_command)
        except Exception as e:
            logger.error(f"Error creating table with SQL command {sql_command}: {e}")
            raise

    def reset_db(self) -> None:
        """Resets the database by dropping it and re-initializing."""
        try:
            self.dropper.dropAllTables()
        except Exception as e:
            logger.error(f"Error resetting the database: {e}")
            raise
