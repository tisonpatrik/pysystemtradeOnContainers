"""
This module provides functionalities for inserting data into a database asynchronously.
"""
from shared.src.utils.logging import AppLogger

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.errors.data_insert_service_errors import (
    DataFrameInsertError,
    TransactionCommitError,
)


class DataInsertService:
    """
    Class for inserting data into a database table asynchronously.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()

    async def async_insert_dataframe_to_table(
        self, data_frame: pd.DataFrame, table_name: str
    ):
        """
        Asynchronously inserts a DataFrame into a PostgreSQL table.

        Args:
            data_frame (pd.DataFrame): The DataFrame to insert.
            table_name (str): The name of the PostgreSQL table.
        """
        try:
            await self.db_session.run_sync(
                lambda session: data_frame.to_sql(
                    table_name, session.bind, index=False, if_exists="append"
                )
            )
            await self.db_session.commit()
            self.logger.info("Data successfully inserted into %s", table_name)

        except (
            DataFrameInsertError,
            TransactionCommitError,
        ) as exc:  # Replace with actual exceptions
            await self.db_session.rollback()
            self.logger.error("An error occurred: %s", exc)
