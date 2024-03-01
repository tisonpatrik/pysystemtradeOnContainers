from uu import Error

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from common.logging.logging import AppLogger


class RecordsRepository:
    """
    SQL Alchemy implementation of the records repository.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_records_async(self, data: pd.DataFrame, table_name: str):
        try:
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
            raise Error(error_message)

    async def fetch_records_async(
        self, table_name: str, conditions: dict
    ) -> pd.DataFrame:
        try:
            query = f"SELECT * FROM {table_name}"
            if conditions:
                condition_str = " AND ".join([f"{k} = :{k}" for k in conditions.keys()])
                query += f" WHERE {condition_str}"
            result = await self.db_session.execute(text(query), conditions or {})
            rows = result.fetchall()
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            return df_result
        except Exception as exc:
            error_message = f"Error fetching data from {table_name}: {exc}"
            self.logger.error(error_message)
            raise Error(error_message)
