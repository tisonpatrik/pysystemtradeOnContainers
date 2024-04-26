import pandas as pd

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger
from risk.src.api.models.queries import AvaragePositionQuery


class InstrumentVolHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_instrument_vol_for_symbol_async(self, position_query: AvaragePositionQuery) -> pd.Series:
        try:
            instrument_volatility = await self._fetch_instrument_volatility(position_query)
            instr_value_vol = self._create_volatility_series(instrument_volatility)
            vol_scalar = self._calculate_volatility_scalar(instr_value_vol, position_query.annual_cash_vol_target)
            self.logger.info("Volatility scalar calculation successful.")
            return vol_scalar
        except Exception as e:
            self.logger.error(f"Error in processing instrument volatility: {str(e)}")
            raise e

    async def _fetch_instrument_volatility(self, position_query: AvaragePositionQuery) -> list:
        query = "SELECT date_time, instrument_volatility FROM instrument_volatility WHERE symbol = $1"
        statement = FetchStatement(query=query, parameters=(position_query.symbol,))
        return await self.repository.fetch_many_async(statement)

    def _create_volatility_series(self, instrument_volatility: list) -> pd.Series:
        df = pd.DataFrame(instrument_volatility)
        return pd.Series(data=df["instrument_volatility"].values, index=pd.to_datetime(df["date_time"]))

    def _calculate_volatility_scalar(self, instr_value_vol: pd.Series, annual_cash_vol_target: float) -> pd.Series:
        return annual_cash_vol_target / instr_value_vol
