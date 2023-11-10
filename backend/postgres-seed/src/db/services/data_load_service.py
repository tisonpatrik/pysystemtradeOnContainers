"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoadService:
    """
    Asynchronous service for loading data from a database table into a Pandas DataFrame.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def fetch_all_from_table_to_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Asynchronously fetches all data from a specified table into a Pandas DataFrame.
        """
        try:
            logger.info("Starting to fetch data from table %s", table_name)
            # Write raw SQL query string
            query_str = f"SELECT * FROM {table_name}"

            # Execute the query asynchronously
            result = await self.db_session.execute(text(query_str))

            # Fetch all rows
            rows = result.fetchall()

            # Create a Pandas DataFrame from the fetched data
            df_result = pd.DataFrame(rows, columns=list(result.keys()))
            return df_result

        except Exception as error:
            logger.error(
                "Failed to fetch data from table %s: %s",
                table_name,
                error,
                exc_info=True,
            )
            raise

    async def fetch_data_from_table_by_symbol(
        self, table_name: str, symbol_value: str
    ) -> pd.DataFrame:
        """
        Asynchronously fetches data by symbol from a specified table into a Pandas DataFrame.
        """
        empty_df = pd.DataFrame()
        try:
            logger.info(
                f"Starting to fetch data from table {table_name} for symbol {symbol_value}"
            )
            # Use parameterized queries to prevent SQL injection
            query_str = f"SELECT * FROM {table_name} WHERE symbol = :symbol_value"

            # Execute the query asynchronously using parameters for security
            result = await self.db_session.execute(
                text(query_str), {"symbol_value": symbol_value}
            )

            # Fetch all rows
            rows = result.fetchall()

            # Check if rows were fetched; if not, return the empty DataFrame
            if not rows:
                logger.info(
                    f"No data found for symbol {symbol_value} in table {table_name}"
                )
                return empty_df

            # Create a Pandas DataFrame from the fetched data
            df_result = pd.DataFrame(rows, columns=list(result.keys()))

            return df_result

        except Exception as error:
            logger.error(
                f"Failed to fetch data from table {table_name}: {error}", exc_info=True
            )
            # Return the empty DataFrame instead of raising the exception to handle the error gracefully
            return empty_df

    async def fetch_data_from_colums_table_by_symbol(
        self, table_name: str, symbol_value: str, columns: list[str]
    ) -> pd.DataFrame:
        """
        Asynchronously fetches specified columns by symbol from a specified table into a Pandas DataFrame.
        """
        empty_df = pd.DataFrame()
        try:
            logger.info(
                f"Starting to fetch data from table {table_name} for symbol {symbol_value}"
            )
            # Convert column list to a comma-separated string for the SQL query
            columns_str = ", ".join(columns)

            # Use parameterized queries to prevent SQL injection
            query_str = (
                f"SELECT {columns_str} FROM {table_name} WHERE symbol = :symbol_value"
            )

            # Execute the query asynchronously using parameters for security
            result = await self.db_session.execute(
                text(query_str), {"symbol_value": symbol_value}
            )

            # Fetch all rows
            rows = result.fetchall()

            # Check if rows were fetched; if not, return the empty DataFrame
            if not rows:
                logger.info(
                    f"No data found for symbol {symbol_value} in table {table_name}"
                )
                return empty_df

            # Create a Pandas DataFrame from the fetched data
            df_result = pd.DataFrame(rows, columns=columns)

            return df_result

        except Exception as error:
            logger.error(
                f"Failed to fetch data from table {table_name}: {error}", exc_info=True
            )
            # Return the empty DataFrame instead of raising the exception to handle the error gracefully
            return empty_df
