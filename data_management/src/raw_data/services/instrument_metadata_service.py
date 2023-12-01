from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import InstrumentMetadataError
from src.raw_data.models.config_models import InstrumentMetadata


class InstrumentMetadataService:
    """
    Service for dealing with operations related to instrument metadata.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_instrument_metadatas_async(self):
        """
        Asynchronously fetch instrument metadatas.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_async(
                InstrumentMetadata.__tablename__
            )
            return data
        except Exception as error:
            self.logger.error(
                "Failed to get instrument metadatas asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentMetadataError("Error fetching instrument metadata", error)
