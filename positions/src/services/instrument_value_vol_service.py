import pandas as pd

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger


class InstrumentValueVolService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_instrument_value_vol(self, instr_ccy_vol: pd.Series, instrument_code: str) -> pd.Series:
        fx_rate = await self._get_fx_rate_async(instrument_code)
        indexed = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
        instr_value_vol = instr_ccy_vol.ffill() * indexed
        return instr_value_vol

    async def _get_fx_rate_async(self, symbol: str) -> pd.Series:
        query = f"""
            SELECT date_time, price
            FROM fx_prices
            WHERE symbol = $1
        """
        statement = FetchStatement(query=query, parameters=(symbol))
        records = await self.repository.fetch_many_async(statement)
        df = pd.DataFrame(records)
        return pd.Series(data=df["price"].values, index=pd.to_datetime(df["date_time"]))
