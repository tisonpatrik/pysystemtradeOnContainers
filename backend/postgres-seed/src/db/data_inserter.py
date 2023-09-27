"""
Module for inserting data into the database asynchronously.

This module provides an asynchronous data inserter class that inserts data 
from a pandas DataFrame into a specified database table. The inserter 
handles database connection and error handling related to database interactions.
"""

import logging

import asyncpg
import pandas as pd

from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    TableOrColumnNotFoundError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataInserter:
    """
    Class responsible for inserting data into a database.
    """

    def __init__(self, database_url: str):
        """
        Initializes the DataInserter with a given database URL.
        """
        self.database_url: str = database_url

    async def insert_dataframe_async(
        self, dataframe: pd.DataFrame, table_name: str
    ) -> None:
        """
        Insert data from a DataFrame into a given table.
        """
        logger.info("Inserting data into %s", table_name)
        pool = await self._create_connection_pool()
        try:
            await self._bulk_insert(pool, dataframe, table_name)
        finally:
            await pool.close()

    async def _create_connection_pool(self) -> asyncpg.pool.Pool:
        """
        Creates a connection pool to the database.
        """
        try:
            logger.info("Creating connection pool.")
            return await asyncpg.create_pool(dsn=self.database_url)
        except asyncpg.exceptions.ConnectionDoesNotExistError as error:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError(
                "Failed to connect to the database."
            ) from error

    async def _bulk_insert(
        self, pool: asyncpg.pool.Pool, dataframe: pd.DataFrame, table_name: str
    ) -> None:
        async with pool.acquire() as conn:
            try:
                await self._insert_records(conn, dataframe, table_name)
            except asyncpg.exceptions.UndefinedTableError as error:
                logger.error("Table or column not defined in SQL: %s", error)
                raise TableOrColumnNotFoundError(
                    f"Table or column not defined: {error}"
                ) from error
            except asyncpg.exceptions.BadCopyFileFormatError as error:
                logger.error("Error during bulk insert: %s", error)
                raise DatabaseInteractionError(
                    f"Error during bulk insert: {error}"
                ) from error
            except Exception as error:
                logger.error("Error inserting data: %s", error)
                raise DatabaseInteractionError(
                    f"Error inserting data: {error}"
                ) from error

    async def _insert_records(
        self,
        conn: asyncpg.connection.Connection,
        dataframe: pd.DataFrame,
        table_name: str,
    ) -> None:
        # Convert DataFrame to a list of records
        records = dataframe.values.tolist()

        # Define columns for the DataFrame
        columns = dataframe.columns.tolist()

        # Insert data into the table
        await conn.copy_records_to_table(table_name, records=records, columns=columns)
