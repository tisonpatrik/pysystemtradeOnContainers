from common.src.cqrs.db_queries.get_point_size import GetPointSize
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
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
        except Exception as e:
            self.logger.error(f"Database error when fetching point size for symbol {symbol}: {e}")
            raise
