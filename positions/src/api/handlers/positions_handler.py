import httpx
import pandas as pd
from fastapi import Depends, HTTPException

from positions.src.api.dependencies.positions_dependencies import get_instrument_value_vol_service
from positions.src.services.cash_volatility_target_service import CashVolTargetService
from positions.src.services.instrument_value_vol_service import InstrumentValueVolService
from positions.src.services.volatility_scalar_service import VolatilityScalarService


class PositionsHandlers:
    def __init__(
        self,
        instrument_value_vol_service: InstrumentValueVolService = Depends(get_instrument_value_vol_service),
    ):
        self.requests_client = httpx.AsyncClient
        self.cash_vol_target_service = CashVolTargetService()
        self.instrument_value_vol_service = instrument_value_vol_service
        self.volatility_scalar_service = VolatilityScalarService()

    async def get_average_position_at_subsystem_level_async(
        self, instrument_code: str, notional_trading_capital: float, percentage_vol_target: float
    ) -> pd.Series:
        instr_ccy_vol = await self.get_instrument_currency_vol(instrument_code)
        instr_value_vol = await self.instrument_value_vol_service.get_instrument_value_vol(
            instr_ccy_vol, instrument_code
        )
        cash_vol_target = self.cash_vol_target_service.get_daily_cash_vol_target(
            notional_trading_capital, percentage_vol_target
        )
        vol_scalar = self.volatility_scalar_service.get_volatility_scalar(cash_vol_target, instr_value_vol)

        return vol_scalar

    async def get_instrument_currency_vol(self, symbol: str) -> pd.Series:
        try:
            response = await self.requests_client().get(
                url=f"http://raw_data:8000/fx_prices_route/get_fx_rate_by_symbol/{symbol}/"
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"Unable to reach the service, details: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch data")
