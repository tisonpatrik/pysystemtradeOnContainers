import logging

from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper
from src.db.schemas.schemas import get_schemas

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, database_url):
        self.config_schemas = get_schemas()
        self.database_url = database_url

    async def init_tables_async(self) -> None:
        """
        Initialize tables in the database using schemas.
        """
        table_creator = TableCreator(self.database_url)
        for schema in self.config_schemas:
            await table_creator.create_table_async(schema.sql_command)

    async def reset_tables_async(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        table_dropper = TableDropper(self.database_url)
        try:
            await table_dropper.drop_all_tables_async()
        except Exception as e:
            logger.error(f"Failed to reset the database: {str(e)}")
            raise e
