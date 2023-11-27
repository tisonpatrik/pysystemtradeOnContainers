"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import pandas as pd
import polars as pl
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.errors.data_loader_service_errors import DataFetchingError


class DataLoadService:
    """
    Asynchronous service for loading data from a database table into a Pandas DataFrame.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_raw_data_from_table_by_symbol(self, table_name: str, symbol: str):
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

            return pl.DataFrame(df_result)

        except Exception as exc:
            self.logger.error(
                f"Failed to fetch data from table {table_name}: {exc}", exc_info=True
            )
            raise DataFetchingError(symbol, exc)

    async def fetch_raw_data_from_table(self, table_name: str):
        try:
            query_str = f"SELECT * FROM {table_name}"
            result = await self.db_session.execute(text(query_str))

            # Asynchronously fetch all rows
            rows = result.fetchall()

            df_result = pd.DataFrame(rows, columns=list(result.keys()))

            return df_result

        except Exception as exc:
            self.logger.error(
                f"Failed to fetch data from table {table_name}: {exc}", exc_info=True
            )
            raise DataFetchingError(exc)
