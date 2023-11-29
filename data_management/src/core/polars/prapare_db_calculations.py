from src.core.data_types_conversion.to_frame import convert_series_to_frame
from src.core.errors.polars_errors import DataPreparationError
from src.core.polars.add_and_populate_column import add_column_and_populate_it_by_value
from src.core.polars.date_time_convertions import convert_datetime_to_unixtime
from src.core.polars.rename_columns import rename_columns
from src.core.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def prepara_data_to_db(prices, model, symbol):
    try:
        framed = convert_series_to_frame(prices)
        column_names = [
            column.name
            for column in model.__table__.columns
            if column.name != model.symbol.name
        ]
        renamed_data = rename_columns(framed, column_names)
        populated = add_column_and_populate_it_by_value(
            data_frame=renamed_data,
            column_name=model.symbol.key,
            column_value=symbol,
        )
        unix_time_converted_data = convert_datetime_to_unixtime(
            populated, model.unix_date_time.name
        )
        return unix_time_converted_data

    except Exception as e:
        logger.error(
            "An error occurred while preparing data for symbol %s: %s",
            symbol,
            e,
            exc_info=True,
        )
        raise DataPreparationError(symbol, str(e))
