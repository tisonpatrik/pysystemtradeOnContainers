"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.data_insert_service import DataInsertService
from src.raw_data.errors.table_to_db_errors import DataInsertionError
from src.raw_data.services.seed_services.mapping_service import MappingService
from src.raw_data.services.seed_services.table_to_db_service import TableToDBService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session: AsyncSession):
        self.mapping_service = MappingService()
        self.table_to_db_service = TableToDBService()
        self.data_insert_service = DataInsertService(db_session)

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """

        mapping = self.mapping_service.load_mappings_from_json()
        datas = self.table_to_db_service.get_processed_data_from_raw_files(mapping)
        for data in datas:
            try:
                await self.data_insert_service.async_insert_dataframe_to_table(
                    data.get_data_frame(), data.get_table_name()
                )
                logger.info("Successfully inserted data into %s", data.get_table_name())

            except Exception as exc:  # Renamed "e" to "exc"
                logger.error(
                    "Error while inserting data into %s: %s",
                    data.get_table_name(),
                    exc,
                    exc_info=True,
                )
                raise DataInsertionError(
                    data.get_table_name(), exc
                ) from exc  # Explicitly re-raise
