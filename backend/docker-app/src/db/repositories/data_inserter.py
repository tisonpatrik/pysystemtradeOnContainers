import asyncpg
import pandas as pd
import logging
from src.db.errors import (DatabaseConnectionError, DatabaseInteractionError,TableOrColumnNotFoundError)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataInserter:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    async def insert_dataframe_async(self, df: pd.DataFrame, table_name: str) -> None:
        logger.info(f"Inserting data into {table_name}.")
        pool = await self._create_connection_pool()
        try:
            await self._bulk_insert(pool, df, table_name)
        finally:
            await pool.close()

    async def _create_connection_pool(self) -> asyncpg.pool.Pool:
        try:
            logger.info("Creating connection pool.")
            return await asyncpg.create_pool(dsn=self.database_url)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.")
    
    async def _bulk_insert(self, pool: asyncpg.pool.Pool, df: pd.DataFrame, table_name: str) -> None:
        async with pool.acquire() as conn:
            try:
                await self._insert_records(conn, df, table_name)
            except asyncpg.exceptions.UndefinedTableError as e:
                logger.error(f"Table or column not defined in SQL: {e}")
                raise TableOrColumnNotFoundError(f"Table or column not defined in SQL: {e}")
            except asyncpg.exceptions.BadCopyFileFormatError as e:
                logger.error(f"Error during bulk insert: {e}")
                raise DatabaseInteractionError(f"Error during bulk insert: {e}")
            except Exception as e:
                logger.error(f"Error inserting data: {e}")
                raise DatabaseInteractionError(f"Error inserting data: {e}")
            
    async def _insert_records(self, conn: asyncpg.connection.Connection, df: pd.DataFrame, table_name: str) -> None:
        # Convert DataFrame to a list of records
        records = df.values.tolist()

        # Define columns for the DataFrame
        columns = df.columns.tolist()

        # Insert data into the table
        await conn.copy_records_to_table(table_name, records=records, columns=columns)


