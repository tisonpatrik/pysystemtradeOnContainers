"""
This module contains a class for truncating all tables from a PostgreSQL database.
"""
import logging
import asyncpg

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseCleaner:
    """
    Represents an interface to delete all data from tables in a PostgreSQL database.
    """

    def __init__(self):
        """
        shit
        """

    async def _get_table_names(self, conn):
        query = "SELECT tablename FROM pg_tables WHERE schemaname = current_schema();"
        rows = await conn.fetch(query)
        return [row["tablename"] for row in rows]

    async def _truncate_table(self, conn, table_name):
        truncate_query = f"TRUNCATE TABLE {table_name} CASCADE;"
        await conn.execute(truncate_query)

    async def truncate_all_tables_async(self):
        async with asyncpg.connect(self.database_url) as conn:
            async with conn.transaction():
                table_names = await self._get_table_names(conn)

                for table_name in table_names:
                    await self._truncate_table(conn, table_name)

        logger.info("Successfully truncated all tables in the database")
