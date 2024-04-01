from typing import Any, Generic, Type, TypeVar

import pandas as pd
from asyncpg import Pool

from common.src.database.base_model import BaseModel
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, pool: Pool, model: Type[T]):
        self.pool = pool
        self.table = model.__tablename__
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_many_async(self, statement: Statement) -> list[dict[Any, Any]]:
        try:
            async with self.pool.acquire() as connectrion:
                async with connectrion.transaction():
                    stmt = await connectrion.prepare(statement.query)
                    records = await stmt.fetch(*statement.parameters)
                    record_dicts = [dict(record) for record in records]
                    return record_dicts
        except Exception as e:
            self.logger.error(f"Failed to fetch data frrom '{self.table}': {e}")
            raise e

    async def insert_dataframe_async(self, data: pd.DataFrame) -> None:
        if data.empty:
            self.logger.warning("Attempted to insert empty data list.")
            return

        records = data.to_numpy()

        try:
            async with self.pool.acquire() as connectrion:
                async with connectrion.transaction():
                    await connectrion.copy_records_to_table(
                        table_name=self.table, records=records, columns=list(data.columns)
                    )
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")
