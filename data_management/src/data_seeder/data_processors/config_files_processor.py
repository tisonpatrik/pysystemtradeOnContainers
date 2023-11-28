from src.core.utils.logging import AppLogger
from src.data_seeder.errors.config_files_errors import ConfigFilesProcessingError
from src.raw_data.utils.filter_dataframe import filter_df_by_symbols
from src.raw_data.utils.rename_columns import rename_columns


class ConfigFilesProcessor:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def process_config_files(self, list_of_symbols, model, raw_data):
        """
        Processes configuration data from a FileTableMapping object.
        """
        try:
            column_names = [column.name for column in model.__table__.columns]
            renamed_data = rename_columns(raw_data, column_names)
            filtered_df = filter_df_by_symbols(renamed_data, list_of_symbols)
            return filtered_df

        except Exception as exc:
            self.logger.error("An unexpected error occurred: %s", exc)
            raise ConfigFilesProcessingError(
                "An unexpected error occurred during processing."
            ) from exc
