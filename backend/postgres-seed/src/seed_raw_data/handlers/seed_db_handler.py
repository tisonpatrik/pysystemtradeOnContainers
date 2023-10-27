"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
import logging

# FastAPI and SQLAlchemy dependencies
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Application-specific dependencies
from src.db.settings.database import get_db

from src.seed_raw_data.services.mapping_service import MappingService
from src.seed_raw_data.services.table_to_db_service import TableToDBService
from src.db.services.data_insert_service import DataInsertService

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
            await self.data_insert_service.async_insert_dataframe_to_table(
                data.get_data_frame(), data.get_table_name()
            )
