"""
bla
"""
import os
import logging

from src.seed_raw_data.schemas.files_mapping import FileTableMapping
from src.data_processor.data_processing.file_path_validator import FilePathValidator
from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.data_processing.tables_helper import TablesHelper
from src.data_processor.data_processing.date_time_helper import DateTimeHelper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdjustedPricesService:
    """
    bla
    """
    def __init__(self):
        self.csv_files_service = CsvFilesService()
        self.file_path_validator = FilePathValidator()
        self.tables_helper = TablesHelper()
        self.date_time_helper = DateTimeHelper()
        self.date_time_column = 'unix_date_time'
        self.price_column = 'price'

    async def process_adjusted_prices(self, map_item: FileTableMapping):
        """
        bla bla
        """
        csv_files_names = [f for f in os.listdir(map_item.directory) if f.endswith('.csv')]
        for csv_file_name in csv_files_names:
            full_path = self.file_path_validator.get_full_path(map_item.directory, csv_file_name)
            name_of_symbol = os.path.splitext(csv_file_name)[0]
            csv = self.csv_files_service.load_csv(full_path)
            renamed = self.tables_helper.rename_columns(csv, map_item.columns_mapping)
            converted_to_date_time = self.date_time_helper.convert_column_to_datetime(renamed, self.date_time_column)
            agregated = self.date_time_helper.aggregate_to_day_based_prices(converted_to_date_time, self.date_time_column)
            coverted_to_unix_time = self.date_time_helper.convert_datetime_to_unixtime(agregated, self.date_time_column)
            rounded = self.tables_helper.round_values_in_column(coverted_to_unix_time,self.price_column)
            symboled = self.tables_helper.add_column_and_populate_it_by_value(rounded,"symbol", name_of_symbol)
