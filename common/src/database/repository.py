from typing import Generic, Type, TypeVar

import pandas as pd
from asyncpg import Pool, Record

from common.src.database.base_model import BaseModel
from common.src.database.statement_factory import StatementFactory
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, pool: Pool, model: Type[T]):
        self.pool = pool
        self.table = model.__tablename__
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_many_async(self, query: str) -> list[Record]:
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    factory = StatementFactory(conn)
                    statement = await factory.create_fetch_many_statement(query)
                    results = await statement.get_statement().fetch(timeout=20)
                    return results
        except Exception as e:
            self.logger.error(f"Failed to fetch data frrom '{self.table}': {e}")
            raise e

    async def insert_dataframe_async(self, data: pd.DataFrame) -> None:
        if data.empty:
            self.logger.warning("Attempted to insert empty data list.")
            return

        records = data.to_numpy()

        try:
            async with self.pool.transaction():
                await self.pool.copy_records_to_table(
                    table_name=self.table, records=records, columns=list(data.columns)
                )
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")
