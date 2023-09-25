"""
Postgres Repository module.

This module provides an interface to interact with a PostgreSQL database, allowing 
operations such as data insertion, loading, table creation, and database reset.
"""

import logging

from src.core.config import settings
from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper

logger = logging.getLogger(__name__)


class PostgresRepository:
    """
    Represents a repository to interact with a PostgreSQL database.
    """

    def __init__(self):
        """
        Initializes the PostgresRepository with necessary database utilities.
        """
        self.inserter = DataInserter(settings.database_url)
        self.loader = DataLoader(settings.database_url)
        self.creator = TableCreator(settings.database_url)
        self.dropper = TableDropper(settings.database_url)

    async def insert_data_async(self, data_frame, table_name):
        """
        Asynchronously inserts data from a DataFrame into a specified table.

        Args:
        - data_frame: The DataFrame containing the data to insert.
        - table_name: The name of the table where the data will be inserted.
        """
        try:
            await self.inserter.insert_dataframe_async(data_frame, table_name)
        except Exception as error:
            logger.error("Error inserting data into %s: %s", table_name, error)
            raise

    async def load_data_async(self, sql_template, parameters ):
        """
        Asynchronously loads data based on the provided SQL template and parameters.

        Args:
        - sql_template: The SQL query template.
        - parameters: A dictionary of parameters to be used in the SQL template.

        Returns:
        A DataFrame containing the loaded data.
        """
        try:
            return await self.loader.fetch_data_async(
                sql_template, parameters
            )
        except Exception as error:
            logger.error(
                "Error loading data with SQL template %s: %s", sql_template, error
            )
            raise

    def create_table(self, sql_command):
        """
        Creates a table in the database using the provided SQL command.

        Args:
        - sql_command: The SQL command to create a table.
        """
        try:
            self.creator.create_table(sql_command=sql_command)
        except Exception as error:
            logger.error(
                "Error creating table with SQL command %s: %s", sql_command, error
            )
            raise

    def reset_db(self):
        """
        Drops all tables in the database to reset it.
        """
        try:
            self.dropper.drop_all_tables()
        except Exception as error:
            logger.error("Error resetting the database: %s", error)
            raise
