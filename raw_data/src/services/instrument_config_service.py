from typing import List

from asyncpg import Connection

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.instrument_config_models import (Instrument,
                                                          InstrumentConfig)


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: Connection):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()
        

    async def get_list_of_instruments_async(self) -> List[InstrumentConfig]:
        """
        Asynchronously fetch instrument consfig data.
        """
        try:
            repository = Repository(self.db_session, InstrumentConfig)
            print(InstrumentConfig.symbol)
            columns = ["symbol"]
            data = await repository.fetch_filtered_data_to_df_async(columns=columns)
            return data
        except Exception as error:
            error_message = f"Failed to get instrument config asynchronously for table '{Instrument.__name__}': {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)