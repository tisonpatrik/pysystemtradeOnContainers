"""
This module provides functionalities for inserting data into a database asynchronously.
"""
import logging

import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataInsertService:
    """
    Class for inserting data into a database table asynchronously.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def async_insert_dataframe_to_table(self, df: pd.DataFrame, table_name: str):
        """
        Asynchronously inserts a DataFrame into a PostgreSQL table.

        Args:
            df (pd.DataFrame): The DataFrame to insert.
            table_name (str): The name of the PostgreSQL table.
        """
        try:
            # Convert DataFrame to SQL and insert into the table
            await self.db_session.run_sync(
                lambda session: df.to_sql(
                    table_name, session.bind, index=False, if_exists="append"
                )
            )
            await self.db_session.commit()  # Commit the transaction
            logger.info(f"Data successfully inserted into {table_name}")

        except Exception as e:
            await self.db_session.rollback()  # Rollback the transaction in case of an error
            logger.error(f"An error occurred: {e}")
