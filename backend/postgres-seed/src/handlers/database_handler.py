"""
Module to handle database operations like table initialization and reset.
"""

import logging

from src.db.repositories.database_cleaner import DatabaseCleaner
from src.handlers.errors import DatabaseError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    A class for handling database-related tasks such as table creation and reset.
    """

    def __init__(self, conn):
        """Initialize the handler with schemas fetched from get_schemas."""
        self.connection = conn

    async def reset_tables_async(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        dropper = DatabaseCleaner(self.connection)
        try:
            await dropper.reset_tables_and_indexes_async()
        except DatabaseError as db_error:  # Catching a more specific exception
            logger.error("Database error while resetting the database: %s", db_error)
            raise DatabaseError("Failed to reset the database.") from db_error
