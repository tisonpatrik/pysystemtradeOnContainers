from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.table_creator import TableCreator
from src.core.config import settings

import pandas as pd

class PostgresRepository:
    def __init__(self):
        self.database_url: str = settings.sync_database_url
        self.loader: DataLoader = DataLoader(self.database_url)

    async def insert_data_async(self, df: pd.DataFrame, table_name: str) -> None:
        inserter = DataInserter(self.database_url)
        await inserter.insert_dataframe_async(df, table_name)

    async def load_data_async(self, sql_template: str, parameters: dict = None) -> pd.DataFrame:
        loader = DataLoader(self.database_url)
        return await loader.fetch_data_as_dataframe_async(sql_template, parameters)
    
    def create_table(self, sql_command: str) -> None:
        creator = TableCreator(self.database_url)
        creator.create_table(sql_command=sql_command)