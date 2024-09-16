from common.src.cqrs.db_queries.get_asset_class import GetAssetClass
from common.src.cqrs.db_queries.get_instruments_for_asset_class import GetInstrumentsForAssetClass
from common.src.cqrs.db_queries.get_point_size import GetPointSize
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.asset_class import AssetClass
from common.src.validation.instrument import Instrument
from common.src.validation.point_size import PointSize


class InstrumentsRepository:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_point_size_async(self, symbol: str) -> PointSize:
        statement = GetPointSize(symbol=symbol)
        try:
            point_size_data = await self.repository.fetch_item_async(statement)
            point_size = to_pydantic(point_size_data, PointSize)
            if point_size is None:
                raise ValueError(f"No data found for symbol {symbol}")
            return point_size
        except Exception:
            self.logger.exception("Database error when fetching point size for symbol '%s'", symbol)
            raise

    async def get_asset_class_async(self, symbol: str) -> AssetClass:
        statement = GetAssetClass(symbol=symbol)
        try:
            asset_class_data = await self.repository.fetch_item_async(statement)
            asset_class = to_pydantic(asset_class_data, AssetClass)
            if asset_class is None:
                raise ValueError(f"No data found for symbol {symbol}")
            return asset_class
        except Exception:
            self.logger.exception("Database error when fetching asset class for symbol '%s'", symbol)
            raise

    async def get_instruments_for_asset_class_async(self, asset_class: str) -> list:
        statement = GetInstrumentsForAssetClass(symbol=asset_class)
        try:
            instruments_data = await self.repository.fetch_many_async(statement)
            return [to_pydantic(instrument, Instrument) for instrument in instruments_data]
        except Exception:
            self.logger.exception("Database error when fetching instruments for asset class '%s'", asset_class)
            raise
