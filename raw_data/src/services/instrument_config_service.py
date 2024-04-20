from pydantic import TypeAdapter

from common.src.database.repository import Repository
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger
from raw_data.src.models.instrument_config_models import AssetClass, Instrument, PointSize


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_list_of_instruments_async(self) -> list[Instrument]:
        """Asynchronously fetch instrument consfig data."""
        try:
            query = "SELECT symbol FROM instrument_config"
            statement = Statement("instrument_config", query, ())
            record_dicts = await self.repository.fetch_many_async(statement)
            instruments = TypeAdapter(list[Instrument]).validate_python(record_dicts)
            return instruments
        except Exception as error:
            error_message = f"Failed to get instrument config asynchronously for table '{Instrument.__name__}': {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_point_size_of_instrument_async(self, symbol: str) -> PointSize:
        """Asynchronously fetch point size for given instrument."""
        try:
            query = "SELECT pointsize FROM instrument_config WHERE symbol = $1"
            statement = Statement("instrument_config", query=query, parameters=symbol)
            record = await self.repository.fetch_item_async(statement)
            point_size = PointSize.model_validate(record)
            return point_size
        except Exception as error:
            error_message = f"Failed to get point size for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_instruments_by_asset_class_async(self, asset_class: AssetClass) -> list[Instrument]:
        """Asynchronously fetch instruments by asset class."""
        try:
            query = "SELECT symbol FROM instrument_config WHERE asset_class = $1"
            statement = Statement("instrument_config", query=query, parameters=asset_class.asset_class)
            record_dicts = await self.repository.fetch_many_async(statement)
            instruments = TypeAdapter(list[Instrument]).validate_python(record_dicts)
            return instruments
        except Exception as error:
            error_message = (
                f"Failed to get instruments by asset class '{asset_class.asset_class}' asynchronously: {error}"
            )
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_asset_classes_async(self) -> list[AssetClass]:
        """Asynchronously fetch asset classes."""
        try:
            query = "SELECT DISTINCT asset_class FROM instrument_config"
            statement = Statement("instrument_config", query, ())
            record_dicts = await self.repository.fetch_many_async(statement)
            asset_classes = TypeAdapter(list[AssetClass]).validate_python(record_dicts)
            return asset_classes
        except Exception as error:
            error_message = f"Failed to get asset classes asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)
