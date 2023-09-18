import logging
from src.db.schemas.config_schemas.instrument_config_schema import InstrumentConfigSchema
from src.db.schemas.config_schemas.instrument_metadata_schema import InstrumentMetadataSchema
from src.db.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db.schemas.config_schemas.spread_cost_schema import SpreadCostSchema
from src.db.repositories.repository import PostgresRepository

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseHandler:

    DEFAULT_SCHEMAS = [
        InstrumentConfigSchema(),
        InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema()
    ]

    def __init__(self, config_schemas=None):
        """Initialize the handler with default or provided config schemas."""
        self.config_schemas = config_schemas or self.DEFAULT_SCHEMAS

    def init_tables(self) -> None:
        """
        Initialize tables in the database using schemas.
        """
        repository = PostgresRepository()
        for schema in self.schemas:
            repository.create_table(schema.sql_command)

    def reset_tables(self) -> None:
        """
        Reset the database by dropping tables and re-initializing.
        """
        repository = PostgresRepository()
        try:
            repository.reset_db()
        except Exception as e:
            logger.error(f"Failed to reset the database: {str(e)}")
            raise e