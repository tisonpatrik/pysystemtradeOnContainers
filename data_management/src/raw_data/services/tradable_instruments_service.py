from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.data_seeder.errors.config_files_errors import TradableInstrumentsServiceError
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.data_seeder.utils.path_validator import get_full_path
from src.db.services.data_insert_service import DataInsertService
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import TradableInstrumentsError
from src.raw_data.models.config_models import TradableInstruments


class TradableInstrumentsService:
    """
    Service for dealing with operations related to tradable instruments.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()
        self.data_insert_service = DataInsertService(db_session)

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

    async def seed_tradable_instruments_files(self):
        """
        Seed tradable instruments data into db.
        """
        try:
            self.logger.info(
                "Starting the process for %s table.", TradableInstruments.tablename
            )
            full_path = get_full_path(
                TradableInstruments.directory, TradableInstruments.file_name
            )
            raw_data = self.csv_loader.load_csv(full_path)

            await self.data_insert_service.async_insert_dataframe_to_table(
                raw_data, TradableInstruments.tablename
            )
        except Exception as exc:
            raise TradableInstrumentsServiceError(
                f"Error seeding config files for {TradableInstruments.tablename}: {str(exc)}"
            )
