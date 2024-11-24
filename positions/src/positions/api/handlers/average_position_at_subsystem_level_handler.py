import pandas as pd

from common.logging.logger import AppLogger
from positions.api.handlers.instrument_value_vol_handler import InstrumentValueVolHandler
from positions.services.cash_volatility_target_service import CashVolTargetService


class AveragePositionAtSubsystemLevelHandler:
    def __init__(self, instrument_value_vol_handler: InstrumentValueVolHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_value_vol_handler = instrument_value_vol_handler
        self.cash_vol_target_service = CashVolTargetService()

    async def get_average_position_at_subsystem_level_async(
        self, symbol: str, base_currency: str, notional_trading_capital: float, percentage_vol_target: float
    ) -> pd.Series:
        instr_value_vol = await self.instrument_value_vol_handler.get_instrument_value_vol(symbol=symbol, base_currency=base_currency)
        cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(notional_trading_capital, percentage_vol_target)
        return cash_vol_target / instr_value_vol
