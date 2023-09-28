import logging
import asyncpg

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TableCreator:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    async def create_table_async(self, sql_command: str):
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
            conn = await asyncpg.connect(self.database_url)

            # Execute the SQL command to create the table
            await conn.execute(sql_command)

            # Log successful table creation
            logger.info(
                f"Successfully executed the following SQL command: {sql_command}"
            )

        except (Exception, asyncpg.DatabaseError) as error:
            logger.error(f"Failed to execute the SQL command due to: {error}")

        finally:
            if conn is not None:
                await conn.close()
                logger.info("Database connection closed.")
