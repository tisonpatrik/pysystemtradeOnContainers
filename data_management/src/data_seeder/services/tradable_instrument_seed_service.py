from src.core.utils.logging import AppLogger
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.db.services.data_insert_service import DataInsertService
from src.core.polars.columns import rename_columns
from src.data_seeder.utils.path_validator import get_full_path
from src.data_seeder.errors.config_files_errors import TradableInstrumentsServiceError

class TradableInstrumentsSeedService:
    """
    Handles the processing of tradable instruments data.
    """
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()
        self.data_insert_service = DataInsertService(db_session)

    async def seed_tradable_instruments_files(self, model):
        """
        Seed tradable instruments data into db.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.tablename)
            full_path = get_full_path(model.directory, model.file_name)
            raw_data = self.csv_loader.load_csv(full_path)
            column_names = list(model.data.__annotations__.keys())
            renamed_data = rename_columns(raw_data, column_names)
            await self.data_insert_service.async_insert_dataframe_to_table(
                renamed_data, model.tablename
            )
        except Exception as exc:
            raise TradableInstrumentsServiceError(
                f"Error seeding config files for {model.tablename}: {str(exc)}"
            )