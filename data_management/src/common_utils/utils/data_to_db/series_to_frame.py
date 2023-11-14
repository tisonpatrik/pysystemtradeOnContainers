import logging

import pandas as pd
from typing import Dict
from src.common_utils.schemas.schema_protocol import SchemaProtocol
from src.common_utils.utils.column_operations.rename_columns import rename_columns
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_datetime_to_unixtime,
)
from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
