"""
This module provides functionalities for inserting data into a database asynchronously.
"""
import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
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
        Asynchronously inserts a DataFrame into a PostgreSQL table.

        Args:
            data_frame (pl.DataFrame): The DataFrame to insert.
            table_name (str): The name of the PostgreSQL table.
        """
        try:
            pandas_data_frame = data_frame.to_pandas()
            await self.db_session.run_sync(
                lambda session: pandas_data_frame.to_sql(
                    table_name, session.bind, index=False, if_exists="append"
                )
            )
            await self.db_session.commit()
        except (DataFrameInsertError,) as exc:
            await self.db_session.rollback()
            self.logger.error("An error occurred: %s", exc)
