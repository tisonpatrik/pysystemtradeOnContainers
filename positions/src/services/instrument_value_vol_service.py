import pandas as pd
from fastapi import HTTPException

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger


class InstrumentValueVolService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def get_instrument_value_vol(self, instrument_code: str) -> pd.Series:
        try:
            self.logger.info(f"Fetching FX rate and currency volatility for {instrument_code}")
            fx_rate = await self._get_fx_rate_async(instrument_code)
            instr_ccy_vol = await self._fetch_instrument_currency_vol(instrument_code)
            indexed = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
            instr_value_vol = instr_ccy_vol.ffill() * indexed
            self.logger.info("Successfully computed instrument value volatility.")
            return instr_value_vol
        except Exception as e:
            self.logger.error(f"Error computing value volatility for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in processing instrument value volatility")

    async def _get_fx_rate_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info(f"Fetching FX rates for {symbol}")
            query = """
                SELECT date_time, price
                FROM fx_prices
                WHERE symbol = $1
            """
            statement = FetchStatement(query=query, parameters=(symbol,))
            records = await self.repository.fetch_many_async(statement)
            df = pd.DataFrame(records)
            return pd.Series(data=df["price"].values, index=pd.to_datetime(df["date_time"]))
        except Exception as e:
            self.logger.error(f"Failed to fetch FX rates for {symbol}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch FX rates for {symbol}")

    async def _fetch_instrument_currency_vol(self, symbol: str) -> pd.Series:
        try:
            self.logger.info(f"Fetching instrument currency volatility for {symbol}")
            query = """
                SELECT date_time, instrument_volatility
                FROM instrument_currency_volatility
                WHERE symbol = $1
            """
            statement = FetchStatement(query=query, parameters=(symbol,))
            records = await self.repository.fetch_many_async(statement)
            df = pd.DataFrame(records)
            return pd.Series(data=df["instrument_volatility"].values, index=pd.to_datetime(df["date_time"]))
        except Exception as e:
            self.logger.error(f"Failed to fetch currency volatility for {symbol}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch currency volatility for {symbol}")
