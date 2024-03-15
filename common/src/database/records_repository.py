from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.base_model import BaseRecord
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseRecord)


class RecordsRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, schema: Type[T]):
        self.db_session = db_session
        self.entity_class = schema
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_raw_data_from_table_by_symbol_async(
        self, table_name: str, symbol: str
    ):
        """
        Asynchronously fetches data by symbol from a specified table into a Pandas DataFrame.
        """
        try:
            # Use parameterized queries to prevent SQL injection
            query_str = "SELECT * FROM {} WHERE symbol = :symbol".format(table_name)
            # Execute the query asynchronously with matching parameter key
            result = await self.db_session.execute(text(query_str), {"symbol": symbol})

            # Fetch all rows
            rows = result.fetchall()

            # Create a Pandas DataFrame from the fetched data
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            return df_result

        except Exception as exc:
            error_message = f"Failed to fetch data from table {table_name} for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def fetch_raw_data_from_table_async(self, table_name: str):
        try:
            query_str = f"SELECT * FROM {table_name}"
            result = await self.db_session.execute(text(query_str))

            # Asynchronously fetch all rows
            rows = result.fetchall()

            df_result = pd.DataFrame(rows, columns=list(result.keys()))

            return df_result

        except Exception as exc:
            error_message = f"Failed to fetch data from table {table_name}: {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def fetch_groupeds_by_column_values_async(
        self, table_name: str, group_by_column: str, concatenate_column: str
    ):
        """
        Asynchronously fetches data from a specified table, groups by one column,
        and concatenates the values from another column.
        """
        try:
            query_str = f"SELECT {group_by_column}, string_agg({concatenate_column}, ', ') AS ConcatenatedValues FROM {table_name} GROUP BY {group_by_column}"
            result = await self.db_session.execute(text(query_str))

            rows = result.fetchall()
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            return df_result

        except Exception as exc:
            error_message = (
                f"Failed to fetch and concatenate data from table {table_name}: {exc}"
            )
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def fetch_rows_by_column_value_async(
        self, table_name: str, column_name: str, column_value: str
    ):
        """
        Asynchronously fetches all rows from a specified table where a given column matches a specific value.
        """
        try:
            query_str = (
                f"SELECT * FROM {table_name} WHERE {column_name} = :column_value"
            )
            result = await self.db_session.execute(
                text(query_str), {"column_value": column_value}
            )

            rows = result.fetchall()
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            return df_result

        except Exception as exc:
            error_message = f"Failed to fetch rows by column {column_name} from table {table_name}: {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def fetch_unique_column_values_async(self, table_name: str, column_name: str):
        """
        Asynchronously fetches unique values from a specified column in a given table.
        """
        try:
            query_str = f"SELECT DISTINCT {column_name} FROM {table_name}"
            result = await self.db_session.execute(text(query_str))

            rows = result.fetchall()
            unique_values = [row[0] for row in rows]

            return unique_values

        except Exception as exc:
            error_message = f"Failed to fetch unique values from column {column_name} in table {table_name}: {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def async_insert_dataframe_to_table(
        self, data_frame: pd.DataFrame, table_name: str
    ):
        """
        Asynchronously inserts a DataFrame into a PostgreSQL table.

        Args:
            data_frame (pl.DataFrame): The DataFrame to insert.
            table_name (str): The name of the PostgreSQL table.
        """
        try:
            await self.db_session.run_sync(
                lambda session: data_frame.to_sql(
                    table_name, session.bind, index=False, if_exists="append"
                )
            )
            await self.db_session.commit()
        except Exception as exc:  # Using a more general exception
            await self.db_session.rollback()
            error_message = f"An error occurred during DataFrame insertion into table {table_name}: {exc}"
            self.logger.error(error_message)
            raise RuntimeError(error_message)
