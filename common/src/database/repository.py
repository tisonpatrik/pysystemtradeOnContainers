from typing import Generic, Type, TypeVar

import pandas as pd
from asyncpg import Connection, Record

from common.src.database.base_model import BaseModel
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, conn: Connection, model: Type[T]):
        self.conn = conn
        self.table = model.__tablename__
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_many_async(self, statemant: Statement) -> list[Record]:

        async with self.conn.transaction():
            try:
                results = await statemant.get_statement().fetch(timeout=20)
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
            async with self.conn.transaction():
                await self.conn.copy_records_to_table(
                    table_name=self.table, records=records, columns=list(data.columns)
                )
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")
