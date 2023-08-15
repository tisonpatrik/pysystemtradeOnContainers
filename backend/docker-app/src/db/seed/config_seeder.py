from src.db.schemas.config_schemas.base_config_schema import BaseConfigSchema
from src.db.repositories.repository import PostgresRepository
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


class ConfigSeeder:
    def __init__(self, schema: BaseConfigSchema):
        self.schema = schema
        self.repository = PostgresRepository()
        self.logger = logging.getLogger(__name__)

    def _load_files(self) -> pd.DataFrame:
        df = pd.read_csv(self.schema.csv_file_path)
        df.rename(columns=self.schema.column_mapping, inplace=True)
        return df
    
    async def _write_records_async(self, df: pd.DataFrame):
        self.repository.create_table(sql_command=self.schema.sql_command)
        await self.repository.insert_data_async(df=df, table_name=self.schema.table_name)
    
    async def seed_async(self):
        self.logger.info(f"Seeding of {self.schema.table_name} table started.")
        df = self._load_files()
        await self._write_records_async(df)
        self.logger.info(f"Seeding of {self.schema.table_name} table finished.")