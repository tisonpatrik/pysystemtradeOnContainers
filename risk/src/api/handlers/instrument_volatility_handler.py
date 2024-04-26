import pandas as pd

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger
from risk.src.api.models.queries import AvaragePositionQuery
from risk.src.schemas.risk_schemas import InstrumentVol
from risk.src.services.instrument_vol_service import InstrumentVolService


class InstrumentVolHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_vol_service = InstrumentVolService()
        self.repository = repository

    async def get_instrument_vol_for_symbol_async(self, position_query: AvaragePositionQuery) -> pd.DataFrame:
        try:
            instrument_volatility = await self._fetch_instrument_volatility(position_query)
            vol_scalar = self.instrument_vol_service.get_instrument_volatility(
                instrument_volatility, position_query.annual_cash_vol_target
            )
            return vol_scalar
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e

    async def _fetch_instrument_volatility(self, position_query: AvaragePositionQuery) -> list:
        # Using Pandera schema to get column names dynamically and safely
        date_time = InstrumentVol.date_time
        instrument_volatility = InstrumentVol.instrument_volatility

        query = f"""
            SELECT {date_time}, {instrument_volatility}
            FROM instrument_currency_volatility
            WHERE symbol = $1
        """
        print(query)

        statement = FetchStatement(query=query, parameters=(position_query.symbol))
        return await self.repository.fetch_many_async(statement)
