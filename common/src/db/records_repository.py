from typing import Any, Dict, Generic, List, Type, TypeVar

import pandas as pd
from asyncpg import Connection
from pandera.typing import DataFrame
from sqlalchemy import table

from common.src.db.base_model import BaseRecord
from common.src.logging.logger import AppLogger
from common.src.validation.base_schema import BaseSchema

T = TypeVar("T", bound=BaseRecord)
S = TypeVar('S', bound=BaseSchema) 

class RecordsRepository(Generic[T, S]):
    def __init__(self, conn: Connection, model: Type[T], schema: Type[S]):
        self.conn = conn
        self.table = model.__tablename__
        self.schema = schema
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_data_async(self, data: DataFrame[S]) -> None:
        """
        Inserts the provided data into the entity's table asynchronously.
        """


    async def fetch_data_to_df_async(self) -> pd.DataFrame:
        """
        Fetches all data from the entity's table asynchronously and loads it into a pandas DataFrame.
        """
        try:
            query = f'SELECT * FROM "{self.table}";'
            records = await self.conn.fetch(query)
            if records:
                columns = [key for key in records[0].keys()]
                df = pd.DataFrame.from_records(data=records, columns=columns)
                return df
            else:
                self.logger.info(
                    f"No data fetched from {self.table}"
                )
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(
                f"Error fetching data from {self.table}: {e}"
            )
            raise

    async def fetch_filtered_data_to_df_async(
        self, filter_by: Dict[str, Any], columns: List[str]
    ) -> pd.DataFrame:
        """
        Fetches filtered data based on the provided conditions and specified columns from the entity's table
        asynchronously and loads it into a pandas DataFrame.

        :param filter_by: Dictionary with {column_name: value} pairs for filtering the data.
        :param columns: List of column names to be fetched.
        """
        try:
            # Prepare the WHERE clause
            where_clause = " AND ".join(
                [
                    f'"{key}" = ${index + 1}'
                    for index, key in enumerate(filter_by.keys())
                ]
            )
            values = list(filter_by.values())

            # Prepare the SELECT clause
            select_clause = ", ".join([f'"{col}"' for col in columns])

            # Construct the query
            query = f'SELECT {select_clause} FROM "{self.table}" WHERE {where_clause};'

            # Execute the query
            records = await self.conn.fetch(query, *values)
            if records:
                df = pd.DataFrame.from_records(data=records, columns=columns)
                return df
            else:
                self.logger.info(
                    f"No data fetched with filter {filter_by} from {self.table}"
                )
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(
                f"Error fetching filtered data from {self.table} with filter {filter_by}: {e}"
            )
            raise
