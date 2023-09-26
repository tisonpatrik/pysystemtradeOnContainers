"""
Postgres Repository module.

This module provides an interface to interact with a PostgreSQL database, allowing 
operations such as data insertion, loading, table creation, and database reset.
"""

import logging
import asyncpg

from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper

logger = logging.getLogger(__name__)


class PostgresRepository:
    """
    Represents a repository to interact with a PostgreSQL database.
    """

    def __init__(self, database_url):
        """
        Initializes the PostgresRepository with necessary database utilities.
        """
        self.database_url = database_url
        self.inserter = DataInserter(database_url)
        self.loader = DataLoader(database_url)
        self.creator = TableCreator(database_url)

    async def connect(self):
        try:
            conn = await asyncpg.connect(self.database_url)
            logger.info("Successfully connected to the database")
            return conn
        except Exception as error:  # or use the specific error type from `asyncpg`
            logger.error(f"Failed to connect to database due to: {error}")
            return None
        
    async def disconnect(self, conn):
        if conn is not None:
            await conn.close()
            logger.info("Database connection closed.")

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

    async def reset_db_async(self):
        """
        
        """
        try:
            connection = await self.connect()
            dropper = TableDropper(connection)            
            await dropper.drop_all_tables()
            await self.disconnect(connection)
        except Exception as error:
            logger.error("Error resetting the database: %s", error)
            raise
