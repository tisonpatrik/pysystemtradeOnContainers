import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from raw_data.src.services.raw_carry_service import RawCarryService


class DailyAnnualisedRollHandler:
    def __init__(self, prices_repository: PricesRepository):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_carry_service = RawCarryService()

    async def get_daily_annualised_roll_async(self, instrument_code: str) -> pd.Series:
        try:
            self.logger.info("Fetching Daily annualised roll for symbol %s", instrument_code)
            raw_carry = await self.prices_repository.get_raw_carry_async(instrument_code)
            rolldiffs = self.raw_carry_service.get_roll_differentials(raw_carry)
            rawrollvalues = self.raw_carry_service.raw_futures_roll(raw_carry)
            annroll = rawrollvalues / rolldiffs
            return annroll.resample("1B").mean()
        except Exception:
            self.logger.exception("Unexpected error occurred while geting Daily annualised roll")
            raise
