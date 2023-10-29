import logging
import pandas as pd
from src.db.services.data_load_service import DataLoadService
from src.raw_data.schemas.adjusted_prices_schema import AdjustedPricesSchema
from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    convert_dataframe_to_dict_of_series,
)
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdjustedPricesService:
    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.schema = AdjustedPricesSchema()

    async def get_adjusted_prices_async(self) -> dict[str, pd.Series]:
        data = await self.data_loader_service.fetch_all_from_table_to_dataframe(
            self.schema.table_name
        )
        series = convert_dataframe_to_dict_of_series(
            data, self.schema.symbol_column, self.schema.index_column
        )
        return series
