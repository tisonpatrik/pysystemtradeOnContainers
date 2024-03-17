import asyncpg
import pandas as pd

from common.src.logging.logger import AppLogger


class Repository:
    """
    Generic repository for CRUD operations on entities.
    """

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_many_async(self, df: pd.DataFrame, table: str) -> None:
        """
        Asynchronously builds and executes a bulk insert query using an asyncpg connection.
        """
        async with self.pool.acquire() as conn:  # Correctly acquiring a connection from the pool
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ",".join(list(df.columns))
            placeholders = ", ".join(["$" + str(i + 1) for i in range(len(tuples[0]))])
            query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
            try:
                await conn.executemany(query, tuples)
                self.logger.info(f"Inserted {len(tuples)} rows into {table}")
            except asyncpg.DatabaseError as error:
                self.logger.error(f"Error executing bulk insert into {table}: {error}")
                raise

    async def fetch_data_to_df_async(self, table_name: str) -> pd.DataFrame:
        """
        Fetches data from the database asynchronously and loads it into a pandas DataFrame.
        """
        return pd.DataFrame()
        # async with self.pool.acquire() as conn:  # Correctly acquiring a connection from the pool
        #     query = f"SELECT * FROM {table_name};"
        #     try:
        #         records = await conn.fetch(query)
        #         if records:
        #             df = pd.DataFrame(records)
        #             df.columns = [key for key in records[0].keys()]
        #             self.logger.info(f"Fetched data from {table_name} into DataFrame")
        #             return df
        #         else:
        #             self.logger.info(f"No data fetched from {table_name}")
        #             return pd.DataFrame()
        #     except Exception as error:
        #         self.logger.error(f"Error fetching data from {table_name}: {error}")
        #         raise
