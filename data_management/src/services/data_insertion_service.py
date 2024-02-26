from src.db.services.data_insert_service import DataInsertService

from common.logging.logging import AppLogger


class GenericDataInsertionService:
    def __init__(self, db_session, table_name):
        self.data_insert_service = DataInsertService(db_session)
        self.table_name = table_name
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_data(self, raw_data, validation_schema):
        """
        Generic method to seed data into db, validating against a given schema.
        """
        try:
            # Validate the raw_data DataFrame against the given schema
            validation_schema.validate(raw_data)
            # Proceed with insertion only if data is valid
            await self.data_insert_service.async_insert_dataframe_to_table(
                raw_data, self.table_name
            )
        except Exception as exc:
            error_message = f"Error seeding data for {self.table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)