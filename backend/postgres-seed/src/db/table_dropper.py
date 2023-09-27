"""
Table Dropper module.

This module provides an interface to drop all tables and indexes from a PostgreSQL database.
"""

import logging

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TableDropper:
    """
    Represents an interface to drop all tables and indexes from a PostgreSQL database.
    """
    def __init__(self, connection):
        self.connection = connection

    async def drop_all_tables(self):
        """
        Drop all tables and indexes from the connected PostgreSQL database.

        Returns:
        - None
        """

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

        async with self.connection.transaction():
            for sql_command in sql_commands:
                await self.connection.execute(sql_command)

        # Log successful table and index drop
        logger.info("Successfully dropped all tables and indexes from the database")

        # Close communication with the PostgreSQL database server
