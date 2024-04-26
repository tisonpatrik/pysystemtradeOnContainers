import pandas as pd
from pandera.typing import Series

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_frame_to_series
from raw_data.src.schemas.raw_data_schemas import DenominatorPricesSchema


class MultiplePricesService:
    """
    Service for dealing with operations related to multiple prices.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_denominator_prices_async(self, symbol: str):
        """
        Asynchronously fetches denominator prices by symbol and returns them as Pandas Series.
        """
        try:
            query = "SELECT price, date_time FROM multiple_prices WHERE symbol = $1 ORDER BY date_time"
            statement = FetchStatement(query=query, parameters=symbol)
            records = await self.repository.fetch_many_async(statement)
            data_frame = pd.DataFrame(records)
            series = convert_frame_to_series(
                data_frame, DenominatorPricesSchema.date_time, DenominatorPricesSchema.price
            )
            validated = Series[DenominatorPricesSchema](series)
            return validated
        except Exception as exc:
            error_message = f"Failed to get adjusted prices asynchronously: {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)
