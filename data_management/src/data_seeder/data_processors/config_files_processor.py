from typing import List

import pandas as pd
from src.core.polars.columns import rename_columns
from src.core.utils.logging import AppLogger
from src.data_seeder.errors.config_files_errors import ConfigFilesProcessingError
from src.data_seeder.utils.filter_dataframe import filter_df_by_symbols

logger = AppLogger.get_instance().get_logger()


def process_config_files(
    list_of_symbols: List[str], raw_data: pd.DataFrame, column_names: List[str]
) -> pd.DataFrame:
    """
    Processes configuration data from a FileTableMapping object.
    """
    try:
        renamed_data = rename_columns(raw_data, column_names)
        filtered_df = filter_df_by_symbols(renamed_data, list_of_symbols)
        return filtered_df

    except Exception as exc:
        logger.error("An unexpected error occurred: %s", exc)
        raise ConfigFilesProcessingError(
            "An unexpected error occurred during processing."
        ) from exc
