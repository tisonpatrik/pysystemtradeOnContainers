import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import TradableInstrumentsError
from src.raw_data.models.config_models import TradableInstrumentsModel
from src.raw_data.schemas.config_schemas import TradableInstrumentsSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


class TradableInstrumentsService:
    """
    Service for dealing with operations related to tradable instruments.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = TradableInstrumentsModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def get_tradable_instruments(self):
        """
        Asynchronously fetch tradable instruments data.
        """
        try:
            data_frame = await self.data_loader_service.fetch_raw_data_from_table_async(
                self.table_name
            )
            symbols_list = data_frame[TradableInstrumentsSchema.symbol].to_list()
            return symbols_list

        except Exception as error:
            self.logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise TradableInstrumentsError("Error fetching instrument config", error)

    async def insert_tradable_instruments_async(self, raw_data: pd.DataFrame):
        """
        Insert tradable instruments data into db.
        """
        try:
            self.logger.info("Starting the process for %s table.", self.table_name)
            await self.data_insertion_service.insert_data(
                raw_data, TradableInstrumentsSchema
            )

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")
