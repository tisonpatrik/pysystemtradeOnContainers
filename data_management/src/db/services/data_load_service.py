"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
from src.utils.logging import AppLogger

import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession

class DataLoadService:
    """
    Asynchronous service for loading data from a database table into a Pandas DataFrame.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()

    def fetch_raw_data_from_table_by_symbol(self, table_name: str, symbol_value: str):
        """
        Fetches data by symbol from a specified table into a Polars DataFrame.
        """
        empty_df = pl.DataFrame()
        try:

            # Use parameterized queries to prevent SQL injection
            query_str = f"SELECT * FROM {table_name} WHERE symbol = '{symbol_value}'"

            # Execute the query synchronously
            df_result = pl.read_database(query=query_str, connection=self.db_session.connection)

            if df_result.is_empty():
                return empty_df

            return df_result

        except Exception as exc:
            self.logger.error(f"Failed to fetch data from table {table_name}: {exc}", exc_info=True)
            return empty_df

    async def fetch_all_from_table_to_dataframe(self, table_name: str):
        """
        Asynchronously fetches all data from a specified table into a Pandas DataFrame.
        """
        empty_df = pl.DataFrame()
        try:
            # Write raw SQL query string
            query_str = f"SELECT * FROM {table_name}"

            # Execute the query asynchronously
            df_result = pl.read_database(query=query_str, connection=self.db_session.connection)

            if df_result.is_empty():
                return empty_df

            return df_result

        except Exception as exc:
            self.logger.error("Failed to fetch data from table %s: %s",table_name,exc,exc_info=True)
            raise
