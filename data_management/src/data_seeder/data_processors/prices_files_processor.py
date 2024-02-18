from src.core.polars.add_and_populate_column import add_column_and_populate_it_by_value
from src.core.polars.columns import rename_columns, retype_dataframe
from src.core.polars.date_time_convertions import (
    convert_datetime_to_unixtime,
    convert_string_column_to_datetime,
)
from src.core.utils.logging import AppLogger
from src.data_seeder.errors.prices_data_seed_error import PricesFilesProcessingError
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.data_seeder.utils.data_aggregators import aggregate_to_day_based_prices
from src.data_seeder.utils.round_column_numbers import round_values_in_column
from src.db.services.data_insert_service import DataInsertService


class PricesFilesProcessor:
    """
    Manages the processing and adjustment of pricing data from CSV files.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader_service = CsvLoaderService()
        self.data_insert_service = DataInsertService(db_session)

    def process_price_files(self, dataframes, model):
        processed_data_frames = []
        for symbol_name, dataframe in dataframes.items():
            try:
                processed_df = self.process_single_dataframe(
                    dataframe, model, symbol_name
                )
                processed_data_frames.append(processed_df)
            except Exception as exc:
                self.logger.error(
                    "An unexpected error occurred while processing data for symbol %s: %s",
                    symbol_name,
                    exc,
                )
                raise PricesFilesProcessingError(
                    f"An unexpected error occurred during processing of data for symbol {symbol_name}."
                ) from exc
        return processed_data_frames

    def process_single_dataframe(self, dataframe, model, symbol_name):
        column_names = [
            column_name
            for column_name in model.data.__annotations__.keys()
            if column_name != "symbol"  # Exclude the 'symbol' column
        ]
        renamed_data = rename_columns(dataframe, column_names)
        date_time_converted_data = convert_string_column_to_datetime(
            renamed_data, "unix_date_time"
        )
        if model.tablename == "roll_calendars":
            final_data = date_time_converted_data 
        else:
            unix_time_converted_data = aggregate_to_day_based_prices(
                date_time_converted_data,
                "unix_date_time",
            )
            rounded_data = round_values_in_column(unix_time_converted_data, "price")
            final_data = rounded_data

        unix_time_converted_data = convert_datetime_to_unixtime(
            final_data, "unix_date_time"
        )
        retype_columns = retype_dataframe(unix_time_converted_data, model.data)
        return add_column_and_populate_it_by_value(
            retype_columns, "symbol", symbol_name
        )
