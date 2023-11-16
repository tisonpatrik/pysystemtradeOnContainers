"""
Handles processing and manipulation of roll calendar data from CSV files.
"""
from src.raw_data.utils.data_aggregators import concatenate_data_frames
from src.raw_data.utils.date_time_convertions import convert_datetime_to_unixtime
from src.raw_data.utils.add_and_populate_column import add_column_and_populate_it_by_value
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.raw_data.services.raw_data_service import RawFilesService

from src.raw_data.core.errors.raw_data_processing_error import ConfigFilesProcessingError, PricesFilesProcessingError
from src.utils.logging import AppLogger

class RollCalendarsService:
    """
    Manages the processing of roll calendar data from CSV files.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader_service = CsvLoaderService()
        self.raw_file_service = RawFilesService()

    def process_roll_calendars(self, model):
        """
        Process and prices for a given table mapping.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)

            dataframes = self.csv_loader_service.load_multiple_csv_files(model.directory)
            processed_data_frames = self._process_csv_files(dataframes, model)
            price_data_frames = concatenate_data_frames(processed_data_frames)
            return price_data_frames
        
        except PricesFilesProcessingError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise
    
    def _process_csv_files(self, dataframes, model):
        """
        Processes each CSV file in the given list.
        """
        processed_data_frames = []
        for symbol_name, dataframe in dataframes.items():
            try:
                preprocessed_data = self.raw_file_service.preprocess_raw_data(dataframe, model, symbol_name)
                unix_time_converted_data = convert_datetime_to_unixtime(preprocessed_data, model.unix_date_time.name)
                processed_df = add_column_and_populate_it_by_value(unix_time_converted_data, model.symbol.name, symbol_name)
                processed_data_frames.append(processed_df)
            except Exception as exc:
                self.logger.error("An unexpected error occurred while processing data for symbol %s: %s", symbol_name, exc)
                raise ConfigFilesProcessingError(f"An unexpected error occurred during processing of data for symbol {symbol_name}.") from exc
        return processed_data_frames

