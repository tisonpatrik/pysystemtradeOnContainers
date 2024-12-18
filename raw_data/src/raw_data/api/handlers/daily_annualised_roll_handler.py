import pandas as pd

from common.src.clients.carry_client import CarryClient
from common.src.logging.logger import AppLogger
from raw_data.services.raw_carry_service import RawCarryService


class DailyAnnualisedRollHandler:
    def __init__(self, carry_client: CarryClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.carry_client = carry_client
        self.raw_carry_service = RawCarryService()

    async def get_daily_annualised_roll_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching Daily annualised roll for symbol %s", symbol)
        raw_carry = await self.carry_client.get_carry_data_async(symbol)
        rolldiffs = self.raw_carry_service.get_roll_differentials(raw_carry)
        rawrollvalues = self.raw_carry_service.raw_futures_roll(raw_carry)
        annroll = rawrollvalues / rolldiffs
        return annroll.resample("1B").mean()
