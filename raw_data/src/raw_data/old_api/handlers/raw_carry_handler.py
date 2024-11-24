import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.old_api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.services.raw_carry_service import RawCarryService
from raw_data.utils.carry import get_raw_carry


class RawCarryHandler:
    def __init__(self, daily_annualised_roll_handler: DailyAnnualisedRollHandler, daily_returns_vol_handler: DailyReturnsVolHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_annualised_roll_handler = daily_annualised_roll_handler
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.raw_carry_service = RawCarryService()

    async def get_raw_carry_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching Raw Carry for symbol %s", symbol)
        annroll = await self.daily_annualised_roll_handler.get_daily_annualised_roll_async(symbol)
        daily_returns_vol = await self.daily_returns_vol_handler.get_daily_returns_vol_async(symbol)
        return get_raw_carry(annroll, daily_returns_vol)
