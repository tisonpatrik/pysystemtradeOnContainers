import pandas as pd

from common.clients.raw_data_client import RawDataClient
from common.logging.logger import AppLogger


class AttenutationHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client

    async def apply_attenutation_to_trading_signal_async(self, symbol: str, raw_signal: pd.Series) -> pd.Series:
        vol_attenutation = await self.raw_data_client.get_vol_attenutation_async(symbol)
        attenuated_forecast = raw_signal * vol_attenutation
        return attenuated_forecast.reindex(raw_signal.index, method="ffill")
