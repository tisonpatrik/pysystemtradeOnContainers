"""
Module for fetching data from the database asynchronously.

This module provides an asynchronous data loader class that fetches data 
from a specified SQL query into a pandas DataFrame. The loader 
handles database connection, error handling related to database interactions, 
and conversion to DataFrame.
"""

import logging

import asyncpg

from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    ParameterMismatchError,
    SQLSyntaxError,
    TableOrColumnNotFoundError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Class responsible for fetching data from a database.
    """

    def __init__(self, database_url):
        """
        Initializes the DataLoader with a given database URL.
        """
        self.database_url = database_url

    async def fetch_data_as_dataframe_async(
        self, sql_template, parameters
    ):
        """
        Fetches data using provided SQL template and returns it as a DataFrame.
        """
        logger.info("Fetching data using provided SQL template.")
        pool = await self._create_connection_pool()
        try:
            rows = await self._execute_sql(pool, sql_template, parameters)
            return rows
        finally:
            await pool.close()

    async def _create_connection_pool(self):
        try:
            logger.info("Creating connection pool.")
            return await asyncpg.create_pool(dsn=self.database_url)
        except asyncpg.exceptions.ConnectionDoesNotExistError as exc:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.") from exc

    async def _execute_sql(
        self, pool, sql_template, parameters
    ):
        async with pool.acquire() as conn:
            try:
                logger.info("Preparing and executing SQL statement.")
                statement = await conn.prepare(sql_template)

                # Create a copy of parameters to avoid side-effects
                params_copy = parameters.copy() if parameters else {}
                if "TABLE" not in sql_template and "TABLE" in params_copy:
                    params_copy.pop("TABLE")

                return await statement.fetch(**params_copy)

            except asyncpg.exceptions.UndefinedTableError as exc:
                logger.error("Table or column not defined in SQL: %s", exc)
                raise TableOrColumnNotFoundError(
                    f"Table or column not defined in SQL: {exc}"
                ) from exc

            except asyncpg.exceptions.SyntaxOrAccessError as exc:
                logger.error("Syntax error or access violation in SQL: %s", exc)
                raise SQLSyntaxError(
                    f"Syntax error or access violation in SQL: {exc}"
                ) from exc

            except asyncpg.exceptions.DataError as exc:
                logger.error("Parameter mismatch or data error: %s", exc)
                raise ParameterMismatchError(
                    f"Parameter mismatch or data error: {exc}"
                ) from exc

            except Exception as exc:
                logger.error("Error executing SQL statement: %s", exc)
                raise DatabaseInteractionError(
                    f"Error executing SQL statement: {exc}"
                ) from exc
