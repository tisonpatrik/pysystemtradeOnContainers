from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.utils.logging import AppLogger


class InstrumentConfigService:
    """
    Handles the processing of instrument config data.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader = CsvLoaderService()
