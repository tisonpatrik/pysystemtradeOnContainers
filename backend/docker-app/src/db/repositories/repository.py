from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.core.config import settings

import pandas as pd

class PostgresRepository:
    def __init__(self):
        self.database_url: str = settings.async_database_url
        self.inserter: DataInserter = DataInserter(self.database_url)
        self.loader: DataLoader = DataLoader(self.database_url)

    async def insert_data_async(self, df: pd.DataFrame, table_name: str) -> None:
        await self.inserter.insert_dataframe_async(df, table_name)

    async def load_data_async(self, sql_template: str, parameters: dict = None) -> pd.DataFrame:
        return await self.loader.fetch_data_as_dataframe_async(sql_template, parameters)
