import logging
import asyncpg
import pandas as pd
from contextlib import asynccontextmanager
from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    TableOrColumnNotFoundError,
)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataInserter:
    def __init__(self, database_url: str):
        self._database_url = database_url

    async def insert_dataframe_async(self, df: pd.DataFrame, table_name: str) -> None:
        async with self._create_connection_pool_async() as pool:
            await self._bulk_insert_async(pool, df, table_name)

    @asynccontextmanager
    async def _create_connection_pool_async(self):
        logger.info("Creating connection pool.")
        try:
            pool = await asyncpg.create_pool(dsn=self._database_url)
            yield pool
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.")
        finally:
            await pool.close()

    async def _bulk_insert_async(self, pool: asyncpg.pool.Pool, df: pd.DataFrame, table_name: str) -> None:
        async with pool.acquire() as conn:
            try:
                await self._insert_records_async(conn, df, table_name)
            except asyncpg.exceptions.UndefinedTableError as e:
                logger.error(f"Table or column not defined in SQL: {e}")
                raise TableOrColumnNotFoundError(f"Table or column not defined in SQL: {e}")
            except Exception as e:
                logger.error(f"Error inserting data: {e}")
                raise DatabaseInteractionError(f"Error inserting data: {e}")

    async def _insert_records_async(self, conn: asyncpg.connection.Connection, df: pd.DataFrame, table_name: str) -> None:
        records = df.values.tolist()
        columns = df.columns.tolist()
        await conn.copy_records_to_table(table_name, records=records, columns=columns)
