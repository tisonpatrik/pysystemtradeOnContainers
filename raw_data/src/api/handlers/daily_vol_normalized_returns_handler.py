import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.risk_client import RiskClient
from raw_data.src.services.daily_vol_normalised_returns_service import DailyVolNormalisedReturnsService


class DailyvolNormalizedReturnsHandler:
    def __init__(self, prices_repository: PricesRepository, risk_client: RiskClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.risk_client = risk_client
        self.daily_vol_normalized_returns_service = DailyVolNormalisedReturnsService()

    async def get_daily_vol_normalised_returns(self, instrument_code: str) -> pd.Series:
        try:
            returnvol_data = await self.risk_client.get_daily_retuns_vol_async(instrument_code)
            prices = await self.prices_repository.get_daily_prices_async(instrument_code)
            norm_return = self.daily_vol_normalized_returns_service.get_daily_vol_normalised_returns(prices, returnvol_data)
            return norm_return
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching Daily volatility normalised returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")
