"""
Table Creator module.

This module provides an interface to create tables in a PostgreSQL database.
"""

import logging

import psycopg2

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableCreator:
    """
    Represents an interface to create tables in a PostgreSQL database.
    """

    def __init__(self, database_url: str):
        """
        Initializes the TableCreator with the provided database URL.

        Args:
        - database_url (str): The URL of the PostgreSQL database to connect to.
        """
        self.database_url: str = database_url

    def create_table(self, sql_command: str):
        """
        Create a table in the PostgreSQL database based on the provided SQL command.

        Args:
        - sql_command (str): SQL command to create a table.

        Returns:
        - None
        """
        conn = None
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(self.database_url)
            cur = conn.cursor()

            # Execute the SQL command to create the table
            cur.execute(sql_command)

            # Commit the changes
            conn.commit()

            # Log successful table creation
            logger.info(
                "Successfully executed the following SQL command: %s", sql_command
            )

            # Close communication with the PostgreSQL database server
            cur.close()

        except psycopg2.DatabaseError as error:
            logger.error("Failed to execute the SQL command due to: %s", error)

        finally:
            if conn is not None:
                conn.close()
                logger.info("Database connection closed.")
