from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

import pandas as pd
from asyncpg import Connection, Record

from common.src.db.base_model import BaseModel
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)

class Repository(Generic[T]):
    def __init__(self, conn: Connection, model: Type[T]):
        self.conn = conn
        self.table = model.__tablename__
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_data_async(self, data: List[T]) -> None:
        """
        Inserts the provided data into the entity's table asynchronously.
        """


    async def fetch_data_async(self) -> List[Record]:
        """
        Fetches all data from the entity's table asynchronously and loads it into a pandas DataFrame.
        """
        try:
            query = f'SELECT * FROM "{self.table}";'
            records = await self.conn.fetch(query)
            if records:
                return records
            else:
                msg = f"No data found in {self.table}"
                self.logger.info(msg)
                raise ValueError(msg)
        except Exception as e:
            self.logger.error(
                f"Error fetching data from {self.table}: {e}"
            )
            raise


    async def fetch_filtered_data_to_df_async(
        self, columns: List[str], filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Record]:
        """
        Fetches data based on the provided conditions (if any) and specified columns from the entity's table asynchronously.

        :param columns: List of column names to be fetched.
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
        

    async def _construct_where_clause(self, filter_by: Dict[str, Any]) -> Tuple[str, List[Any]]:
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