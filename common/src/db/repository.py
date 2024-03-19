from typing import Any, Dict, Generic, Optional, Tuple, Type, TypeVar

import pandas as pd
from asyncpg import Connection, Record
from asyncpg.prepared_stmt import PreparedStatement

from common.src.db.base_model import BaseModel
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)

class Repository(Generic[T]):
    def __init__(self, conn: Connection, model: Type[T]):
        self.conn = conn
        self.table = model.__tablename__
        self.logger = AppLogger.get_instance().get_logger()

            
    async def fetch_many_async(self, prepared_statement:PreparedStatement)->list[Record]:
        async with self.conn.transaction():
            try:
               results = await prepared_statement.fetch(timeout=20)
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
                    table_name=self.table,
                    records=records,
                    columns=list(data.columns))
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")

    async def fetch_filtered_data_to_df_async(
        self, columns: list[str], filter_by: Optional[Dict[str, Any]] = None
    ) -> list[Record]:
        """
        Fetches data based on the provided conditions (if any) and specified columns from the entity's table asynchronously.

        :param columns: list of column names to be fetched.
        :param filter_by: Optional dictionary with {column_name: value} pairs for filtering the data.
        """
        try:
            where_clause, values = await self._construct_where_clause(filter_by if filter_by else {})
            
            select_clause = ", ".join([f'"{col}"' for col in columns])
            query = f'SELECT {select_clause} FROM "{self.table}"{where_clause};'
            
            records = await self.conn.fetch(query, *values)
            if records:
                return records
            else:
                msg = f"No data found in {self.table}"
                if filter_by:
                    msg += f" with filter {filter_by}"
                msg += f" for columns {columns}"
                self.logger.info(msg)
                raise ValueError(msg)
        except Exception as error:
            error_msg = f"Error fetching data from {self.table}"
            if filter_by:
                error_msg += f" with filter {filter_by}"
            error_msg += f" for columns {columns}: {error}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from error
        

    async def _construct_where_clause(self, filter_by: Dict[str, Any]) -> Tuple[str, list[Any]]:
        """
        Constructs a WHERE clause for SQL queries based on the provided filtering criteria.

        :param filter_by: Dictionary with {column_name: value} pairs for filtering the data.
        :return: A tuple containing the WHERE clause as a string and a list of values for parameter substitution.
        """
        where_clause = ""
        values = []
        if filter_by:
            where_clause = " WHERE " + " AND ".join(
                [f'"{key}" = ${index + 1}' for index, key in enumerate(filter_by.keys())]
            )
            values = list(filter_by.values())
        return where_clause, values