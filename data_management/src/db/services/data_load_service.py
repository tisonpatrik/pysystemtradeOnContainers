"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.errors.data_loader_service_errors import (
    DataFetchingError,
    EmptyDataFrameError,
)
from src.utils.logging import AppLogger


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
        Raises an EmptyDataFrameError if the result is an empty DataFrame.
        """
        try:
            # Use parameterized queries to prevent SQL injection
            query_str = "SELECT * FROM {} WHERE symbol = %s".format(table_name)
            parameters = (symbol_value,)

            # Execute the query synchronously
            df_result = pl.read_database(
                query=query_str,
                parameters=parameters,
                connection=self.db_session.connection,
            )

            if df_result.is_empty():
                raise EmptyDataFrameError(
                    f"No data found in table {table_name} for symbol {symbol_value}"
                )

            return df_result

        except Exception as exc:
            self.logger.error(
                f"Failed to fetch data from table {table_name}: {exc}", exc_info=True
            )
            raise DataFetchingError(table_name, exc)
