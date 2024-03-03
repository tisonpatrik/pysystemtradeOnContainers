from src.utils.converter import convert_series_to_frame
from src.utils.table_operations import (
    add_column_and_populate_it_by_value,
    rename_columns,
)

from common.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


def prepara_data_to_db(prices, model, symbol):
    try:
        prices.dropna(inplace=True)
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
        return populated

    except Exception as error:
        error_message = (
            f"An error occurred while preparing data for symbol'{symbol}'. {error}"
        )
        logger.error(error_message, exc_info=True)
        raise ValueError(error_message)


def prepare_asset_data_to_db(prices, model, asset):
    try:
        framed = convert_series_to_frame(prices)
        column_names = [
            column.name
            for column in model.__table__.columns
            if column.name != model.asset_class.name
        ]
        renamed_data = rename_columns(framed, column_names)
        populated = add_column_and_populate_it_by_value(
            data_frame=renamed_data,
            column_name=model.asset_class.key,
            column_value=asset,
        )
        return populated
    except Exception as error:
        error_message = (
            f"An error occurred while preparing data for symbol'{asset}'. {error}"
        )
        logger.error(error_message, exc_info=True)
        raise ValueError(error_message)
