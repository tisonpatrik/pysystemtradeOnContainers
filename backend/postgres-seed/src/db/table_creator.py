"""
Table Creator module.

This module provides an interface to create tables in a PostgreSQL database.
"""

import logging

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableCreator:
    """
    Represents an interface to create tables in a PostgreSQL database.
    """

    def __init__(self, connection):
        """
        Initializes the TableCreator with the provided database URL.

        Args:
        - database_url (str): The URL of the PostgreSQL database to connect to.
        """
        self.connection = connection

    async def create_table_async(self, sql_command: str):
        try:
            await self.connection.execute(sql_command)
            logger.info("Successfully executed the following SQL command: %s", sql_command)
        except Exception as error:
            logger.error("Failed to execute the SQL command due to: %s", error)
        finally:
            logger.info("Database connection closed.")
