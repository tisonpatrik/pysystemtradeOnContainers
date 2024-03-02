from typing import Generic, Type, TypeVar

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.db_service.models.record_mode import RecordModel
from common.database.db_service.repositories.records_repository import RecordsRepository
from common.logging.logging import AppLogger
from common.utils.converter import convert_frame_to_series
from common.utils.table_operations import sort_by_time

T = TypeVar("T", bound=RecordModel)


class SeriesRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, series_class: Type[T]):
        self.records_repository = RecordsRepository(db_session)
        self.series_class = series_class
        self.logger = AppLogger.get_instance().get_logger()

    async def get_series_async(self, table_name: str) -> pd.Series:
        data_frame = await self.records_repository.fetch_records_async(table_name)
        sorted_by_time = sort_by_time(data_frame, self.series_class.time_column)
        series = convert_frame_to_series(
            sorted_by_time,
            self.series_class.time_column,
            self.series_class.price_column,
        )
        return series

    async def insert_series_async(self, series: pd.Series, table_name: str):
        df = series.to_frame()
        await self.records_repository.insert_records_async(df, table_name)
