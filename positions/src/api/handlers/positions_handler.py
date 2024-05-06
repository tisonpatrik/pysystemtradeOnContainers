import pandas as pd
from fastapi import Depends, HTTPException

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_client, get_repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.models.api_query_models import GetFxRateQuery, GetInstrumentCurrencyVolQuery
from positions.src.api.models.positions_request_model import SubsystemPositionForInstrument
from positions.src.services.cash_volatility_target_service import CashVolTargetService


class PositionsHandlers:
    def __init__(
        self,
        repository: Repository = Depends(get_repository),
        client: RestClient = Depends(get_client),
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.repository = repository
        self.client = client

    async def get_subsystem_position_async(self, request: SubsystemPositionForInstrument) -> pd.Series:
        try:
            self.logger.info("Starting to get average position at subsystem level.")
            avg_abs_forecast = request.avarage_absolute_forecas

            fx_rate = await self.get_fx_rates_async(request.instrument_code, request.base_currency)
            instr_ccy_vol = await self.get_instrument_volatility_async(request.instrument_code)
            indexed = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
            instr_value_vol = instr_ccy_vol.ffill() * indexed
            cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(
                request.notional_trading_capital, request.percentage_volatility_target
            )
            vol_scalar = cash_vol_target / instr_value_vol

            # forecast = self.get_combined_forecast(request.instrument_code)
            # vol_scalar_reindexed = vol_scalar.reindex(forecast.index, method="ffill")
            # subsystem_position_raw = vol_scalar_reindexed * forecast / avg_abs_forecast
            # subsystem_position = self._apply_long_only_constraint_to_position(
            #     positions=subsystem_position_raw, instrument_code=request.instrument_code
            # )
            self.logger.info("Successfully computed average position.")
            return vol_scalar
        except Exception as e:
            self.logger.error("Failed to compute average position: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    def get_combined_forecast(self, instrument_code: str):
        return pd.Series(1)

    def _apply_long_only_constraint_to_position(self, positions: pd.Series, instrument_code: str) -> pd.Series:
        return positions

    async def get_fx_rates_async(self, instrument_code: str, base_currency: str) -> pd.Series:
        try:
            self.logger.info(f"Fetching FX rate for {instrument_code}")
            get_fx_rate_query = GetFxRateQuery(symbol=instrument_code, base_currency=base_currency)
            fx_rate = await self.client.get_data_async(get_fx_rate_query)
            self.logger.info("Successfully fetched FX rate.")
            return pd.Series(fx_rate)
        except Exception as e:
            self.logger.error(f"Error fetching FX rate for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching FX rate")

    async def get_instrument_volatility_async(self, instrument_code: str) -> pd.Series:
        try:
            self.logger.info(f"Fetching instrument volatility for {instrument_code}")
            get_instrument_vol_query = GetInstrumentCurrencyVolQuery(symbol=instrument_code)
            instr_vol = await self.client.get_data_async(get_instrument_vol_query)
            self.logger.info("Successfully fetched instrument volatility.")
            return pd.Series(instr_vol)
        except Exception as e:
            self.logger.error(f"Error fetching instrument volatility for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching instrument volatility")
