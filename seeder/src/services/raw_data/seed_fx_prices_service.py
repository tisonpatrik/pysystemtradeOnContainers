import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import FxPricesModel


class SeedFxPricesService:
    """
    Service for dealing with operations related to fx prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, FxPricesModel)

    async def seed_fx_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert fx prices data into db.
        """
        try:
            data = [FxPricesModel(**row.to_dict()) for _, row in raw_data.iterrows()]
            await self.repository.insert_many_async(data)

        except Exception as exc:
            self.logger.error(
                f"Error inserting data for {FxPricesModel.__tablename__}: {str(exc)}"
            )
