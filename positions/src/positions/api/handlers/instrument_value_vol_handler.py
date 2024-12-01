import pandas as pd

from common.clients.old_raw_data_client import RawDataClient
from common.logging.logger import AppLogger
from positions.services.cash_volatility_target_service import CashVolTargetService


class InstrumentValueVolHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.cash_vol_target_service = CashVolTargetService()
        self.raw_data_client = raw_data_client

    async def get_instrument_value_vol(self, symbol: str, base_currency: str) -> pd.Series:
        self.logger.info("Starting to get instrument value vol.")
        instr_ccy_vol = await self.raw_data_client.get_instrument_volatility_async(symbol)
        fx_rate = await self.raw_data_client.get_fx_prices_async(symbol, base_currency)
        fx_rate = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
        return instr_ccy_vol.ffill() * fx_rate
