import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.db.services.data_load_service import DataLoadService
from src.raw_data.csv_to_db_configs.config_files_config import TradableInstrumentsConfig
from src.raw_data.errors.config_files_errors import TradableInstrumentsError
from src.raw_data.errors.tradable_service_erros import TradableInstrumentsServiceError
from src.raw_data.schemas.config_schemas import TradableInstrumentsSchema
from src.raw_data.utils.csv_loader import get_full_path, load_csv


class TradableInstrumentsService:
    """
    Service for dealing with operations related to tradable instruments.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)

    async def get_tradable_instruments(self):
        """
        Asynchronously fetch tradable instruments data.
        """
        try:
            data_frame = await self.data_loader_service.fetch_raw_data_from_table_async(
                TradableInstrumentsConfig.tablename
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

    async def seed_tradable_instruments_files(self):
        """
        Seed tradable instruments data into db.
        """
        try:
            self.logger.info(
                "Starting the process for %s table.",
                TradableInstrumentsConfig.tablename,
            )
            full_path = get_full_path(
                TradableInstrumentsConfig.directory, TradableInstrumentsConfig.file_name
            )
            raw_data = load_csv(full_path)

            # Validate the raw_data DataFrame against the schema
            TradableInstrumentsSchema.validate(raw_data)
            raw_data = pl.DataFrame(raw_data)
            # Proceed with insertion only if data is valid
            await self.data_insert_service.async_insert_dataframe_to_table(
                raw_data, TradableInstrumentsConfig.tablename
            )
        except Exception as exc:
            self.logger.error(
                f"Error seeding config files for {TradableInstrumentsConfig.tablename}: {str(exc)}"
            )
            raise TradableInstrumentsServiceError(
                f"Error seeding config files for {TradableInstrumentsConfig.tablename}: {str(exc)}"
            )
