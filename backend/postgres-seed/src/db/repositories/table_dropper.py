"""
Table Dropper module.

This module provides an interface to drop all tables and indexes from a PostgreSQL database.
"""

import logging

import psycopg2

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableDropper:
    """
    Represents an interface to drop all tables and indexes from a PostgreSQL database.
    """

    def __init__(self, database_url: str):
        """
        Initializes the TableDropper with the provided database URL.

        Args:
        - database_url (str): The URL of the PostgreSQL database to connect to.
        """
        self.database_url: str = database_url

    def drop_all_tables(self):
        """
        Drop all tables and indexes from the connected PostgreSQL database.

        Returns:
        - None
        """
        conn = None
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(self.database_url)
            cur = conn.cursor()

            # Generate the SQL command to drop all tables
            drop_tables_command = (
                "DO $$ DECLARE r RECORD; "
                "BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) "
                "LOOP EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE'; "
                "END LOOP; END $$;"
            )

            drop_indexes_command = (
                "DO $$ DECLARE r RECORD; "
                "BEGIN FOR r IN (SELECT indexname FROM pg_indexes WHERE schemaname = current_schema()) "
                "LOOP EXECUTE 'DROP INDEX IF EXISTS ' || r.indexname || ' CASCADE'; "
                "END LOOP; END $$;"
            )

            sql_commands = [drop_tables_command, drop_indexes_command]

            for sql_command in sql_commands:
                cur.execute(sql_command)

            # Committing the changes to the database
            conn.commit()

            # Log successful table and index drop
            logger.info("Successfully dropped all tables and indexes from the database")

            # Close communication with the PostgreSQL database server
            cur.close()

        except psycopg2.DatabaseError as error:
            logger.error("Failed to drop tables/indexes due to: %s", error)

        finally:
            if conn is not None:
                conn.close()
                logger.info("Database connection closed.")
