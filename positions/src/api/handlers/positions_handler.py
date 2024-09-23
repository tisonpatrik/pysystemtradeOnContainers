import pandas as pd

from common.src.cqrs.api_queries.get_fx_rate import GetFxRateQuery
from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.cqrs.api_queries.get_subsystem_positions import GetSubsystemPositionForInstrument
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from positions.src.services.cash_volatility_target_service import CashVolTargetService


class PositionsHandler:
    def __init__(self, repository: Repository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.repository = repository
        self.client = client

    async def get_subsystem_position_async(self, request: GetSubsystemPositionForInstrument) -> pd.Series:
        try:
            self.logger.info("Starting to get average position at subsystem level.")

            fx_rate = await self.get_fx_rates_async(request.symbol, request.base_currency)
            instr_ccy_vol = await self.get_instrument_volatility_async(request.symbol)
            indexed = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
            instr_value_vol = instr_ccy_vol.ffill() * indexed
            cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(
                request.notional_trading_capital, request.percentage_volatility_target
            )
            vol_scalar = cash_vol_target / instr_value_vol

            self.logger.info("Successfully computed average position.")
            return vol_scalar
        except Exception:
            self.logger.exception("Failed to compute average position")
            raise

    def get_combined_forecast(self, instrument_code: str):
        self.logger.info("Fetching combined forecast for %s", instrument_code)

        return pd.Series()

    def _apply_long_only_constraint_to_position(self, positions: pd.Series, instrument_code: str) -> pd.Series:
        return positions

    async def get_fx_rates_async(self, instrument_code: str, base_currency: str) -> pd.Series:
        try:
            get_fx_rate_query = GetFxRateQuery(symbol=instrument_code, base_currency=base_currency)
            fx_rate = await self.client.get_data_async(get_fx_rate_query)
            self.logger.info("Successfully fetched FX rate.")
            return pd.Series(fx_rate)
        except Exception:
            self.logger.exception("Error fetching FX rate for %s", instrument_code)
            raise

    async def get_instrument_volatility_async(self, instrument_code: str) -> pd.Series:
        try:
            get_instrument_vol_query = GetInstrumentCurrencyVolQuery(symbol=instrument_code)
            instr_vol = await self.client.get_data_async(get_instrument_vol_query)
            self.logger.info("Successfully fetched instrument volatility.")
            return pd.Series(instr_vol)
        except Exception:
            self.logger.exception("Error fetching instrument volatility for %s", instrument_code)
            raise
