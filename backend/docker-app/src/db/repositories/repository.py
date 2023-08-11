from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.core.config import settings

import pandas as pd

class PostgresRepository:
    def __init__(self):
        self.database_url: str = settings.async_database_url
        self.inserter: DataInserter = DataInserter(self.database_url)
        self.loader: DataLoader = DataLoader(self.database_url)

    async def insert_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        await self.inserter.insert_dataframe(df, table_name)

    async def load_data(self, sql_template: str, parameters: dict = None) -> pd.DataFrame:
        return await self.loader.fetch_data_as_dataframe(sql_template, parameters)
