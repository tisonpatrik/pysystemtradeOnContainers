"""
Module to handle database operations like table initialization and reset.
"""

import logging
from src.db.repositories.repository import PostgresRepository
from src.db.schemas.schemas import get_schemas
from src.handlers.errors import DatabaseError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    A class for handling database-related tasks such as table creation and reset.
    """
    def __init__(self):
        """Initialize the handler with schemas fetched from get_schemas."""
        self.config_schemas = get_schemas()

    def init_tables(self) -> None:
        """
        Initialize tables in the database using the SQL commands defined in the schemas.
        """
        repository = PostgresRepository()
        for schema in self.config_schemas:
            repository.create_table(schema.sql_command)

    async def reset_tables(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        repository = PostgresRepository()
        try:
           await repository.reset_db_async()
        except Exception as error:
            logger.error("Failed to reset the database: %s", str(error))
            raise DatabaseError("Failed to reset the database.") from error
