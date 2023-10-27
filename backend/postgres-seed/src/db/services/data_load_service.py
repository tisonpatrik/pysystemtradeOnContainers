"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoadService:
    """
    Asynchronous service for loading data from a database table into a Pandas DataFrame.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def fetch_all_from_table_to_dataframe(self, table_name: str) -> pd.DataFrame:
        try:
            logger.info(f"Starting to fetch data from table {table_name}")
            # Write raw SQL query string
            query_str = f"SELECT * FROM {table_name}"

            # Execute the query asynchronously
            result = await self.db_session.execute(text(query_str))

            # Fetch all rows
            rows = result.fetchall()

            # Create a Pandas DataFrame from the fetched data
            result = pd.DataFrame(rows, columns=list(result.keys()))
            return result

        except Exception as e:
            logger.error(
                f"Failed to fetch data from table {table_name}: {e}", exc_info=True
            )
            raise
