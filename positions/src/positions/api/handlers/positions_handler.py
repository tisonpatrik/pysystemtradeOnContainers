import pandas as pd

from common.src.clients.raw_data_client import RawDataClient
from common.src.cqrs.api_queries.get_subsystem_positions import GetSubsystemPositionForInstrument
from common.src.logging.logger import AppLogger
from positions.services.cash_volatility_target_service import CashVolTargetService


class PositionsHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.raw_data_client = raw_data_client

    async def get_subsystem_position_async(self, request: GetSubsystemPositionForInstrument) -> pd.Series:
        try:
            self.logger.info("Starting to get average position at subsystem level.")

            fx_rate = await self.raw_data_client.get_fx_prices_async(request.symbol, request.base_currency)
            instr_ccy_vol = await self.raw_data_client.get_instrument_volatility_async(request.symbol)
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
