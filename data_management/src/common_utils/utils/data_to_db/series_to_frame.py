import logging

import pandas as pd
from typing import Dict
from src.common_utils.schemas.schema_protocol import SchemaProtocol
from src.raw_data.utils.rename_columns import rename_columns
from src.raw_data.utils.date_time_convertions import convert_datetime_to_unixtime
from src.raw_data.utils.add_and_populate_column import add_column_and_populate_it_by_value
from src.utils.logging import AppLogger

logger = AppLogger.get_instance().get_logger()


def process_series_to_frame(
    series: pd.Series, symbol: str, schema: SchemaProtocol, mapping: Dict[str, str]
) -> pd.DataFrame:
    data_frame = pd.DataFrame(series)
    data_frame.reset_index(inplace=True)
    renamed = rename_columns(data_frame, mapping)
    unix_timed = convert_datetime_to_unixtime(renamed, schema.unix_date_time.key)
    populated = add_column_and_populate_it_by_value(
        unix_timed, schema.symbol.key, symbol
    )
    return populated
