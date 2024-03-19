from asyncpg import Connection
from pydantic import TypeAdapter

from common.src.db.repository import Repository
from common.src.db.statement_factory import StatementFactory
from common.src.logging.logger import AppLogger
from raw_data.src.models.instrument_config_models import (Instrument,
                                                          InstrumentConfig)
from raw_data.src.schemas.config_files_schemas import InstrumentConfigSchema


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: Connection):
        self.db_session = db_session
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(self.db_session, InstrumentConfig)
        self.statement_factory = StatementFactory(self.db_session, InstrumentConfig.__tablename__)


    async def get_list_of_instruments_async(self) -> list[Instrument]:
        """
        Asynchronously fetch instrument consfig data.
        """
        try:
            columns = [InstrumentConfigSchema.symbol]
            statement = await self.statement_factory.create_fetch_all_statement(columns)
            records = await self.repository.fetch_many_async(statement)
            record_dicts = [dict(record) for record in records]
            instruments = TypeAdapter(list[Instrument]).validate_python(record_dicts)
            return instruments
        except Exception as error:
            error_message = f"Failed to get instrument config asynchronously for table '{Instrument.__name__}': {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)