import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from raw_data.src.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.src.services.raw_carry_service import RawCarryService


class RawCarryHandler:
    def __init__(self, daily_annualised_roll_handler: DailyAnnualisedRollHandler, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_annualised_roll_handler = daily_annualised_roll_handler
        self.raw_data_client = raw_data_client
        self.raw_carry_service = RawCarryService()

    async def get_raw_carry_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Fetching Raw Carry for symbol %s", symbol)
            annroll = await self.daily_annualised_roll_handler.get_daily_annualised_roll_async(symbol)
            daily_returns_vol = await self.raw_data_client.get_daily_returns_vol_async(symbol)
            return self.raw_carry_service.get_raw_carry(annroll, daily_returns_vol)
        except Exception:
            self.logger.exception("Unexpected error occurred while geting Raw Carry")
            raise
