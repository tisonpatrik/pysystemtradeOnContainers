"""
Module to handle database operations like truncate of tables and returning of list of tables.
"""

import logging

from src.handlers.errors import DatabaseError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    A class for handling database-related tasks such as table creation and reset.
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize the handler with schemas fetched from get_schemas."""
        self.db_session = db_session

    async def truncate_tables_async(self) -> None:
        """
        Truncate all tables in the database,
        effectively deleting all records but keeping the schema.
        """
        try:
            # Get the list of all tables
            query = text(
                "SELECT tablename FROM pg_catalog.pg_tables "
                "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
            )

            tables = await self.db_session.execute(query)
            table_list = tables.fetchall()

            # Truncate each table
            for table in table_list:
                truncate_query = text(
                    f"TRUNCATE TABLE {table[0]} RESTART IDENTITY CASCADE;"
                )
                await self.db_session.execute(truncate_query)

            # Commit the changes
            await self.db_session.commit()

            logger.info("Successfully truncated all tables.")

        except Exception as e:
            logger.error("Failed to truncate tables: %s", e)
            await self.db_session.rollback()
            raise DatabaseError("Failed to truncate tables.") from e

    async def list_tables_async(self) -> list:
        """
        Returns a list of all table names in the database.
        """
        try:
            query = text(
                "SELECT tablename FROM pg_catalog.pg_tables "
                "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
            )
            result = await self.db_session.execute(query)
            tables = [row[0] for row in result.fetchall()]

            logger.info(
                "Successfully fetched %d table names from the database.", len(tables)
            )
            return tables
        except Exception as e:
            logger.error("Failed to fetch table names: %s", e)
            raise DatabaseError("Failed to fetch table names from the database.") from e
