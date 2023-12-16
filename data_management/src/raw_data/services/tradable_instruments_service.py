from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.models.config_models import TradableInstruments
from src.raw_data.errors.config_files_errors import TradableInstrumentsError

class TradableInstrumentsService:
    """
    Service for dealing with operations related to tradable instruments.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_tradable_instruments(self):
        """
        Asynchronously fetch tradable instruments data.
        """
        try:
            data_frame = await self.data_loader_service.fetch_raw_data_from_table_async(
                TradableInstruments.__tablename__
            )
            symbols_list = data_frame[TradableInstruments.symbol.key].to_list()
            return symbols_list
        
        except Exception as error:
            self.logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise TradableInstrumentsError("Error fetching instrument config", error)