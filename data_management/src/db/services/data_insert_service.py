"""
This module provides functionalities for inserting data into a database asynchronously.
"""
from src.utils.logging import AppLogger

import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, table, column
from sqlalchemy.exc import SQLAlchemyError
from src.db.errors.data_insert_service_errors import DataFrameInsertError


class DataInsertService:
    """
    Class for inserting data into a database table asynchronously.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()

    async def async_insert_dataframe_to_table(
        self, data_frame: pl.DataFrame, table_name: str
    ):
        """
        Asynchronously inserts a Polars DataFrame into a PostgreSQL table.

        Args:
            data_frame (pl.DataFrame): The DataFrame to insert.
            table_name (str): The name of the PostgreSQL table.
        """
        try:
            # Convert Polars DataFrame to list of dictionaries for insertion
            data_dicts = data_frame.to_dicts()

            # Create a SQLAlchemy table object dynamically
            dynamic_table = table(table_name,*[column(name) for name in data_frame.columns])

            # Perform the insert operation
            await self.db_session.execute(insert(dynamic_table).values(data_dicts))
            await self.db_session.commit()

        except SQLAlchemyError as exc:  # Adjust exception as needed
            await self.db_session.rollback()
            self.logger.error("An error occurred: %s", exc)
            raise DataFrameInsertError(table_name, str(exc)) from exc
