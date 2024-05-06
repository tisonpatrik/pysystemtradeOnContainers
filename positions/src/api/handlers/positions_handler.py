import pandas as pd
from fastapi import Depends, HTTPException

from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement
from common.src.logging.logger import AppLogger
from positions.src.api.dependencies.positions_dependencies import get_repository
from positions.src.api.models.positions_request_model import SubsystemPositionForInstrument
from positions.src.services.cash_volatility_target_service import CashVolTargetService
from positions.src.services.volatility_scalar_service import VolatilityScalarService


class PositionsHandlers:
    def __init__(
        self,
        repository: Repository = Depends(get_repository),
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.volatility_scalar_service = VolatilityScalarService()
        self.repository = repository

    async def get_subsystem_position_async(self, request: SubsystemPositionForInstrument) -> pd.Series:
        try:
            self.logger.info("Starting to get average position at subsystem level.")
            avarage_forecast = request.avarage_absolute_forecas

            # vol scalar

            instr_value_vol = await self.get_instrument_value_vol(request.instrument_code, request.base_currency)
            cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(
                request.notional_trading_capital, request.percentage_volatility_target
            )
            vol_scalar = self.volatility_scalar_service.get_volatility_scalar(cash_vol_target, instr_value_vol)

            # forecast

            self.logger.info("Successfully computed average position.")
            return vol_scalar
        except Exception as e:
            self.logger.error("Failed to compute average position: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    async def get_instrument_value_vol(self, instrument_code: str, base_currency: str) -> pd.Series:
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
            statement = FetchStatement(query=query, parameters=("EURUSD"))
            records = await self.repository.fetch_many_async(statement)
            df = pd.DataFrame(records)
            return pd.Series(data=df["price"].values, index=pd.to_datetime(df["date_time"]))
        except Exception as e:
            self.logger.error(f"Failed to fetch FX rates for {symbol}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch FX rates for {symbol}")

    async def _get_instrument_currency(self, symbol: str) -> str:
        try:
            self.logger.info(f"Fetching instrument currency for {symbol}")
            query = """
                SELECT currency
                FROM instrument_config
                WHERE symbol = $1 
            """
            statement = FetchStatement(query=query, parameters=(symbol,))
            record = await self.repository.fetch_item_async(statement)
            record = str(record)
            return record
        except Exception as e:
            self.logger.error(f"Failed to fetch instrument currency for {symbol}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch instrument currency for {symbol}")

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
