"""
Module to handle database operations like table initialization and reset.
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

    async def reset_tables_async(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        try:
            # Get the list of all tables
            query = text(
                "SELECT tablename FROM pg_catalog.pg_tables "
                "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
            )

            tables = await self.db_session.execute(query)
            table_list = tables.fetchall()

            # Drop each table
            for table in table_list:
                drop_query = text(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
                await self.db_session.execute(drop_query)

            # Commit the changes
            await self.db_session.commit()

            logger.info("Successfully dropped all tables.")

        except Exception as e:
            logger.error("Failed to drop tables: %s", e)
            await self.db_session.rollback()
            raise DatabaseError("Failed to reset database.") from e
