"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.data_insert_service import DataInsertService
from src.raw_data.core.errors.table_to_db_errors import DataInsertionError
from src.raw_data.services.table_to_db_service import TableToDBService
from src.raw_data.models.config_schemas import InstrumentConfig, InstrumentMetadata ,RollConfig, SpreadCost
from src.utils.logging import AppLogger

class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_to_db_service = TableToDBService()
        self.data_insert_service = DataInsertService(db_session)
        

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        models = [InstrumentConfig, InstrumentMetadata, RollConfig, SpreadCost]

        for model in models:
            print(model.file_name)


        # mapping = self.mapping_service.load_mappings_from_json()
        # datas = self.table_to_db_service.get_processed_data_from_raw_files(mapping)
        # for data in datas:
        #     try:
        #         await self.data_insert_service.async_insert_dataframe_to_table(
        #             data.data_frame, data.table_name
        #         )
        #         self.logger.info("Successfully inserted data into %s", data.table_name)

        #     except Exception as exc:  # Renamed "e" to "exc"
        #         self.logger.error(
        #             "Error while inserting data into %s: %s",
        #             data.table_name,
        #             exc,
        #             exc_info=True,
        #         )
        #         raise DataInsertionError(
        #             data.table_name, exc
        #         ) from exc  # Explicitly re-raise
