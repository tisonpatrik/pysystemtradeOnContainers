import pandas as pd
from common.clients.prices_client import PricesClient
from common.logging.logger import AppLogger

from raw_data.services.raw_carry_service import RawCarryService
from raw_data.utils.carry import raw_futures_roll


class DailyAnnualisedRollHandler:
    def __init__(self, prices_client: PricesClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_client = prices_client
        self.raw_carry_service = RawCarryService()

    async def get_daily_annualised_roll_async(self, symbol: str) -> pd.Series:
        self.logger.info('Fetching Daily annualised roll for symbol %s', symbol)
        raw_carry = await self.prices_client.get_carry_data_async(symbol)
        rolldiffs = self.raw_carry_service.get_roll_differentials(raw_carry)
        rawrollvalues = raw_futures_roll(raw_carry)
        annroll = rawrollvalues / rolldiffs
        return annroll.resample('1B').mean()
