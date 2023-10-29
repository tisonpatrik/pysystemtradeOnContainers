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
