from src.core.polars.add_and_populate_column import add_column_and_populate_it_by_value
from src.core.polars.date_time_convertions import (
    convert_datetime_to_unixtime,
    convert_string_column_to_datetime,
)
from src.core.polars.rename_columns import rename_columns
from src.core.utils.logging import AppLogger
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.db.services.data_insert_service import DataInsertService
from src.raw_data.errors.raw_data_processing_error import PricesFilesProcessingError
from src.raw_data.utils.data_aggregators import aggregate_to_day_based_prices
from src.raw_data.utils.round_column_numbers import round_values_in_column


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
            column.name
            for column in model.__table__.columns
            if column.name != model.symbol.name
        ]
        renamed_data = rename_columns(dataframe, column_names)
        date_time_converted_data = convert_string_column_to_datetime(
            renamed_data, model.unix_date_time.name
        )

        if model.__tablename__ == "roll_calendars":
            final_data = date_time_converted_data
        else:
            unix_time_converted_data = aggregate_to_day_based_prices(
                date_time_converted_data,
                model.unix_date_time.name,
                model.price.name,
            )
            rounded_data = round_values_in_column(
                unix_time_converted_data, model.price.name
            )
            final_data = rounded_data

        unix_time_converted_data = convert_datetime_to_unixtime(
            final_data, model.unix_date_time.name
        )
        return add_column_and_populate_it_by_value(
            unix_time_converted_data, model.symbol.name, symbol_name
        )
