import pandas as pd
from fastapi import Depends, HTTPException

from common.src.logging.logger import AppLogger
from positions.src.api.dependencies.positions_dependencies import get_instrument_value_vol_service
from positions.src.services.cash_volatility_target_service import CashVolTargetService
from positions.src.services.instrument_value_vol_service import InstrumentValueVolService
from positions.src.services.volatility_scalar_service import VolatilityScalarService


class PositionsHandlers:
    def __init__(
        self,
        instrument_value_vol_service: InstrumentValueVolService = Depends(get_instrument_value_vol_service),
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.instrument_value_vol_service = instrument_value_vol_service
        self.volatility_scalar_service = VolatilityScalarService()

    async def get_average_position_at_subsystem_level_async(
        self, instrument_code: str, notional_trading_capital: float, percentage_vol_target: float
    ) -> pd.Series:
        try:
            self.logger.info("Starting to get average position at subsystem level.")
            instr_value_vol = await self.instrument_value_vol_service.get_instrument_value_vol(instrument_code)
            cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(
                notional_trading_capital, percentage_vol_target
            )
            vol_scalar = self.volatility_scalar_service.get_volatility_scalar(cash_vol_target, instr_value_vol)
            self.logger.info("Successfully computed average position.")
            return vol_scalar
        except Exception as e:
            self.logger.error("Failed to compute average position: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))
