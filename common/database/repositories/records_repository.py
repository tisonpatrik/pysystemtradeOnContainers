from typing import Generic, Optional, TypeVar

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models.base_model import BaseModel
from common.logging.logger import AppLogger
from common.utils.table_operations import sort_by_time

T = TypeVar("T", bound=BaseModel)


class RecordsRepository(Generic[T]):
    """
    SQL Alchemy implementation of the records repository.
    """

    def __init__(self, db_session: AsyncSession, series_schema):
        self.db_session = db_session
        self.series_schema = series_schema
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_records_async(
        self, table_name: str, condition: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            query = f"SELECT * FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            result = await self.db_session.execute(text(query))
            rows = result.fetchall()
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            sorted_by_time = sort_by_time(df_result, self.series_schema.time_column)
            return sorted_by_time
        except Exception as exc:
            error_message = f"Error fetching data from {table_name} with condition [{condition}]: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def insert_records_async(self, data: pd.DataFrame, table_name: str):
        try:
            self.series_schema.validate(data)
            await self.db_session.run_sync(
                lambda session: data.to_sql(
                    table_name, session.bind, if_exists="append", index=False
                )
            )
            await self.db_session.commit()
        except Exception as exc:
            await self.db_session.rollback()
            error_message = f"Error inserting data into {table_name}: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)
