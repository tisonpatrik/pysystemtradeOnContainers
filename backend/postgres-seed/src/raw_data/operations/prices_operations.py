from curses import raw
import os
import pandas as pd

from src.raw_data.schemas.files_mapping import FileTableMapping
from src.raw_data.utils.path_validator import get_full_path
from src.raw_data.utils.csv_loader import load_csv

from src.common_utils.utils.rename_columns import rename_columns, remove_unnamed_columns
from src.common_utils.utils.round_column_numbers import round_values_in_column
from src.common_utils.utils.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)


def process_single_csv_file(
    csv_file_name: str,
    map_item: FileTableMapping,
    price_column: str,
    date_time_column: str,
    symbol_column: str,
) -> pd.DataFrame:
    """
    Process a single CSV file and return a processed DataFrame.
    """
    full_path = get_full_path(map_item.directory, csv_file_name)
    symbol_name = os.path.splitext(csv_file_name)[0]

    raw_data = load_csv(full_path)
    removed_unnamed_columns = remove_unnamed_columns(raw_data)
    renamed_data = rename_columns(removed_unnamed_columns, map_item.columns_mapping)
    aggregated_data = (
        date_time_service.aggregate_string_datetime_column_to_day_based_prices(
            renamed_data, date_time_column
        )
    )
    rounded_data = round_values_in_column(aggregated_data, price_column)

    return add_column_and_populate_it_by_value(rounded_data, symbol_column, symbol_name)
