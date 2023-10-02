"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import logging

import asyncpg
import pandas as pd

from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    ParameterMismatchError,
    SQLSyntaxError,
    TableOrColumnNotFoundError,
)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, database_url):
        self.database_url = database_url

    async def fetch_data_as_dataframe_async(self, sql_query):
        logger.info(f"Fetching data using SQL query: {sql_query}.")
        
        conn = await asyncpg.connect(dsn=self.database_url)
        try:
            rows = await conn.fetch(sql_query)
        except asyncpg.SyntaxOrAccessError as exc:
            logger.error(f"SQL syntax or access error occurred: {exc}. Query: {sql_query}")
            raise SQLSyntaxError from exc
        except asyncpg.ConnectionFailureError as exc:
            logger.error(f"Database connection error: {exc}.")
            raise DatabaseConnectionError from exc
        except Exception as exc:
            logger.error(f"An unexpected error occurred: {exc}. Query: {sql_query}")
            raise DatabaseInteractionError from exc
        finally:
            await conn.close()

        return self._convert_to_dataframe(rows)

    def _convert_to_dataframe(self, rows):
        logger.info("Converting fetched rows to DataFrame.")
        
        if not rows:
            logger.warning("No rows fetched. Returning an empty DataFrame.")
            return pd.DataFrame()

        try:
            columns = [desc[0] for desc in rows[0].keys()]
        except IndexError:
            logger.error("Could not determine DataFrame column names.")
            raise ParameterMismatchError("No column names found.")

        return pd.DataFrame(rows, columns=columns)


